from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any, List, Optional
import os
import uuid

from . import mcp_server as mcp_tools

app = FastAPI(title="sustiai API", version="0.1.0")


@app.on_event("startup")
def _setup_loop_exception_filter():
    """Install an event-loop exception handler that filters out a noisy
    anyio/stdio cancel-scope RuntimeError seen while shutting down the
    mcp stdio client. This prevents the runtime error stack trace from
    being printed to the server logs for normal shutdown scenarios.
    """
    import asyncio

    loop = asyncio.get_event_loop()
    prev = loop.get_exception_handler()

    def _handler(loop, context):
        exc = context.get("exception")
        if exc is None:
            # nothing to do — preserve default behaviour
            if prev:
                return prev(loop, context)
            return

        # Detect the specific cancel-scope runtime error and quietly ignore it
        msg = str(exc)
        if isinstance(exc, RuntimeError) and "Attempted to exit cancel scope" in msg:
            return

        # For ExceptionGroups / BaseExceptionGroup from anyio, the message
        # may include the same text — filter that too.
        if "Attempted to exit cancel scope" in msg:
            return

        # Otherwise delegate to the previous handler if available
        if prev:
            return prev(loop, context)
        # fallback: re-raise so default machinery handles it
        raise exc


@app.get("/health")
def health() -> dict:
    """Simple healthcheck endpoint."""
    return {"status": "ok"}


@app.get("/events/{event_id}/kpis")
def event_kpis(event_id: int) -> Any:
    res = mcp_tools.get_event_kpis(event_id)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=404, detail=res.get("error"))
    return res


@app.get("/events/{event_id}/breakdown")
def event_breakdown(event_id: int) -> Any:
    return mcp_tools.get_event_emissions_breakdown(event_id)


@app.get("/companies/{company_id}/summary")
def company_summary(company_id: int) -> Any:
    res = mcp_tools.get_company_portfolio_summary(company_id)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=404, detail=res.get("error"))
    return res


@app.get("/companies/{company_id}/monthly")
def company_monthly(company_id: int, year: str) -> List[dict]:
    return mcp_tools.get_company_monthly_emissions(company_id, year)


@app.get("/search")
def search(q: str) -> Any:
    """Search entities by text. Example: /search?q=Tech"""
    return mcp_tools.search_entities(q)


class SQLRequest(BaseModel):
    query: str


@app.post("/run_sql")
def run_sql_endpoint(req: SQLRequest) -> Any:
    resp = mcp_tools.run_sql(req.query)
    # If run_sql returned an error wrapper, return 400
    error_condition = (
        isinstance(resp, list)
        and len(resp)
        and isinstance(resp[0], dict)
        and resp[0].get("error")
    )
    if error_condition:
        raise HTTPException(status_code=400, detail=resp[0].get("error"))
    return resp


@app.get("/branding/{company_id}")
def branding(company_id: int) -> Any:
    res = mcp_tools.get_branding_config(company_id)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=404, detail=res.get("error"))
    return res


class AgentQuery(BaseModel):
    query: str
    save_path: Optional[str] = None


@app.post("/run_agent_report")
def run_agent_report_endpoint(req: AgentQuery):
    """Run an agentic workflow for the given user query and return HTML.

    This endpoint uses the mcp_server helpers for a deterministic fallback
    path when the ADK/agent runner is not available in the environment.
    """
    query = req.query

    # If an ADK orchestrator exists we'd prefer to use it, but in most CI
    # environments the orchestrator is not available. Use a simple fallback.
    try:
        from .agents import orchestrator

        if getattr(orchestrator, "HAS_ADK", False):
            runner = orchestrator.runner
            if hasattr(runner, "run_debug") and hasattr(runner, "session_service"):
                # Attempt a best-effort run with the real runner
                async def _run_async():
                    session = await runner.session_service.create_session(app_name="reporting_app", user_id="api_user")
                    response = await runner.run_debug(query, session_id=session.id, verbose=True)
                    return response

                import asyncio

                response = asyncio.run(_run_async())

                # Best-effort: try to find and return HTML the agents produced
                def _extract_html(obj) -> str | None:
                    """Recursively walk the response object to find an HTML string or
                    a saved file path (reports/*.html). Returns the found HTML or
                    None if not found.
                    """
                    import os
                    import re

                    def walk(o):
                        found = []
                        # direct string
                        if isinstance(o, str):
                            found.append(o)
                            return found
                        # dict / mapping
                        if isinstance(o, dict):
                            for v in o.values():
                                found.extend(walk(v))
                            return found
                        # iterable
                        if isinstance(o, (list, tuple, set)):
                            for v in o:
                                found.extend(walk(v))
                            return found
                        # objects with attributes -> try __dict__
                        try:
                            d = getattr(o, "__dict__", None)
                            if d:
                                found.extend(walk(d))
                        except Exception:
                            pass
                        return found

                    strings = walk(obj)

                    # First look for raw HTML snippets
                    for s in strings:
                        if not isinstance(s, str):
                            continue
                        if "<!DOCTYPE html>" in s or "<html" in s or "<body" in s:
                            start = s.find("<!DOCTYPE html>")
                            if start == -1:
                                start = s.find("<html")
                            end = s.rfind("</html>")
                            if end != -1:
                                return s[start : end + len("</html>")]
                            return s[start:]

                    # Next look for saved report paths (reports/*.html) and return file contents
                    for s in strings:
                        if not isinstance(s, str):
                            continue
                        m = re.search(r"(reports[\\/][^\s'\"]+\.html)", s)
                        if m:
                            candidate = m.group(1)
                            # ensure path is safe & exists
                            if os.path.exists(candidate):
                                try:
                                    with open(candidate, "r", encoding="utf-8") as fh:
                                        return fh.read()
                                except Exception:
                                    continue

                    return None

                html = _extract_html(response)
                if html:
                    return HTMLResponse(content=html)

                return {"ok": True, "agent_response": str(response)}
    except Exception:
        # Any failure should fall back to a deterministic DB-backed report
        pass

    # Fallback reporting path using mcp_tools
    # Search for entities which names are contained inside the query text.
    # Use SQL 'query LIKE %name%' so queries like 'report for Sustainability
    # Summit ...' still match the event named 'Sustainability Summit'.
    events = mcp_tools.query(
        "SELECT e.id, e.name, e.start_time, c.name as company_name FROM event e JOIN company c ON e.company_id = c.id WHERE ? LIKE '%' || e.name || '%'",
        (query,),
    )

    companies = mcp_tools.query("SELECT id, name FROM company WHERE ? LIKE '%' || name || '%'", (query,))

    if not events and not companies:
        raise HTTPException(status_code=404, detail="No such events found")

    if events:
        event_id = events[0]["id"]
        kpis = mcp_tools.get_event_kpis(event_id)
        breakdown = mcp_tools.get_event_emissions_breakdown(event_id)
        # Attempt to find company id and branding
        conn_info = mcp_tools.query("SELECT company_id FROM event WHERE id = ?", (event_id,))
        branding = None
        if conn_info and conn_info[0].get("company_id"):
            branding = mcp_tools.get_branding_config(conn_info[0].get("company_id"))

        from typing import cast

        # Build quick HTML
        html = ["<html><body>", f"<h1>{kpis.get('event_name', 'Event')}</h1>", f"<h2>{kpis.get('company_name','')}</h2>", "<h3>KPIs</h3>", "<pre>", str(kpis), "</pre>", "<h3>Breakdown</h3>", "<pre>", str(breakdown), "</pre>"]
        if branding:
            html.extend(["<h4>Branding</h4>", "<pre>", str(branding), "</pre>"])
        html.append("</body></html>")

        html_text = "\n".join(cast(list, html))

        # Save report file
        os.makedirs("reports", exist_ok=True)
        out_path = req.save_path or f"reports/report_{uuid.uuid4().hex}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_text)

        return HTMLResponse(content=html_text)

    # Company-level fallback
    company_id = companies[0]["id"]
    summary = mcp_tools.get_company_portfolio_summary(company_id)
    monthly = mcp_tools.get_company_monthly_emissions(company_id, year=str(os.getenv("REPORT_YEAR", "2025")))
    html = ["<html><body>", f"<h1>{summary.get('company_name','')}</h1>", "<pre>", str(summary), "</pre>", "<pre>", str(monthly), "</pre>", "</body></html>"]
    html_text = "\n".join(html)
    out_path = req.save_path or f"reports/report_{uuid.uuid4().hex}.html"
    os.makedirs("reports", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_text)

    return HTMLResponse(content=html_text)
