"""FastAPI entrypoint for local development / production.

Small runner that exposes the `src.sustiai.api` FastAPI application as
an ASGI app for uvicorn / WSGI servers.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import uuid
import os
from pathlib import Path

try:
    # Import the app from the package
    from src.sustiai.api import app
    from src.sustiai.agents import orchestrator
    from src.sustiai import mcp_server
except Exception:  # pragma: no cover - runtime entrypoint
    # Fallback: create a minimal app so importing main won't fail in tests
    app = FastAPI()
    orchestrator = None
    mcp_server = None


def _install_loop_exception_filter():
    """Install a local event-loop exception filter similar to the API app
    so runtime noise from anyio / mcp stdio shutdown doesn't pollute
    the console output when the orchestrator performs stdio cleanups.
    """
    try:
        import asyncio

        loop = asyncio.get_event_loop()
        prev = loop.get_exception_handler()

        def _handler(loop, context):
            exc = context.get("exception")
            if exc is None:
                if prev:
                    return prev(loop, context)
                return

            msg = str(exc)
            if isinstance(exc, RuntimeError) and "Attempted to exit cancel scope" in msg:
                return
            if "Attempted to exit cancel scope" in msg:
                return

            if prev:
                return prev(loop, context)
            raise exc

        loop.set_exception_handler(_handler)
    except Exception:
        # Non-fatal best-effort; we should never crash because of the filter
        pass

# Ensure a /health endpoint exists on the app even when falling back
try:
    # Some environments import the app from src.sustiai.api which already
    # defines /health. If not, add a minimal healthcheck so tooling can
    # reliably probe the service.
    if not any(r.path == "/health" for r in app.routes):
        @app.get("/health")
        def _health() -> dict:  # simple liveness probe
            return {"status": "ok"}
except Exception:
    # Be defensive — ensure this file never raises during import time.
    pass


class AgentQuery(BaseModel):
    query: str
    save_path: Optional[str] = None


def _build_html_report(event_kpis: dict, breakdown: list, branding: dict | None = None) -> str:
    """Create a simple HTML report from the provided payload.

    This keeps the original notebook prompts and logic untouched while providing
    a simple visual output in environments without the ADK agents.
    """
    title = event_kpis.get("event_name", "Event Report")
    company = event_kpis.get("company_name", "Unknown")

    html = [
        "<html>",
        "<head><meta charset=\"utf-8\"><title>%s</title></head>" % title,
        "<body style='font-family: Arial, sans-serif; margin: 30px;'>",
        f"<header><h1>{title}</h1><h3>{company}</h3></header>",
        "<section>",
        "<h2>Key KPIs</h2>",
        "<table border=\"1\" cellpadding=\"8\" style=\"border-collapse:collapse;\">",
        "<tbody>",
    ]

    for k, v in event_kpis.items():
        if k in ("event_name", "company_name"):
            continue
        html.append(f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>")

    html.extend(["</tbody>", "</table>", "</section>", "<section>", "<h2>Emissions breakdown</h2>", "<ul>"])

    for r in breakdown:
        html.append(f"<li>{r.get('scope_name','')}: {r.get('category_name','')} — {r.get('total_kg',0)}</li>")

    html.extend(["</ul>", "</section>"])

    if branding:
        html.append("<footer>Branding:<pre>%s</pre></footer>" % (branding,))

    html.append("</body></html>")
    return "\n".join(html)


@app.post("/run_agent_report")
def run_agent_report(payload: AgentQuery):
    """Run the agentic reporting pipeline for a user query and return HTML.

    Behavior:
    - If `src.sustiai.agents.orchestrator` exists and looks like a real runner
      (HAS_ADK True and runner supports run_debug), attempt to run the
      configured pipeline and return its report output.
    - Otherwise run a safe fallback that uses `mcp_server` tools to produce a
      small HTML report for the top matching event.
    """
    query = payload.query

    # Real agent flow (best-effort): try running the orchestrator runner
    try:
        if orchestrator is not None and getattr(orchestrator, "HAS_ADK", False):
            runner = orchestrator.runner
            # The real ADK runner is asynchronous. Use `run_debug` if available.
            if hasattr(runner, "run_debug") and hasattr(runner, "session_service"):
                async def _run_async():
                    session = await runner.session_service.create_session(app_name="reporting_app", user_id="api_user")
                    response = await runner.run_debug(query, session_id=session.id, verbose=True)
                    return response

                # Run and attempt to extract a usable HTML report string
                response = asyncio.run(_run_async())

                # Best-effort: extract HTML from the ADK runner response (handles
                # nested structures and saved-file references) and return only the
                # HTML body. If extraction fails, return a textual fallback.
                def _extract_html(obj) -> str | None:
                    import os, re

                    def walk(o):
                        out = []
                        if isinstance(o, str):
                            out.append(o)
                            return out
                        if isinstance(o, dict):
                            for v in o.values():
                                out.extend(walk(v))
                            return out
                        if isinstance(o, (list, tuple, set)):
                            for v in o:
                                out.extend(walk(v))
                            return out
                        try:
                            d = getattr(o, "__dict__", None)
                            if d:
                                out.extend(walk(d))
                        except Exception:
                            pass
                        return out

                    strings = walk(obj)
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

                    # check for saved report paths and return file contents.
                    # Support paths with spaces and both relative (reports/...) and
                    # absolute Windows or Unix paths.
                    path_patterns = [
                        r"(reports[\\/][^'\"\n\r]+?\.html)",
                        r"([A-Za-z]:[\\/][^'\"\n\r]+?\.html)",
                        r"(/[^'\"\n\r]+?\.html)",
                    ]

                    for s in strings:
                        if not isinstance(s, str):
                            continue
                        candidate = None
                        for pat in path_patterns:
                            m = re.search(pat, s)
                            if m:
                                candidate = m.group(1)
                                break

                        if candidate:
                            tried = [candidate, os.path.join(os.getcwd(), candidate)]
                            try:
                                candidate_norm = os.path.normpath(candidate)
                                tried.extend([candidate_norm, os.path.join(os.getcwd(), candidate_norm)])
                            except Exception:
                                pass

                            for p in tried:
                                if not isinstance(p, str):
                                    continue
                                if os.path.exists(p):
                                    try:
                                        with open(p, "r", encoding="utf-8") as fh:
                                            return fh.read()
                                    except Exception:
                                        continue

                    return None
                
                try:

                    report_text = response[-1].content.parts[0].text  # Get the text
                    import re
                    match = re.search(r'"(reports/[^"]+)"', report_text)
                    report_path = match.group(1) if match else None
                    print("Found the path", report_path)
                    with open(report_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    return HTMLResponse(content=html_content)


                except Exception:
                    html = _extract_html(response)
                    if html:
                        return HTMLResponse(content=html)

                return {"ok": True, "agent_response": str(response[-1].content.parts[0].text)}
    except Exception:
        # If the ADK run fails, fall back to safe path below
        pass

    # Fallback: run simple DB-backed flow using mcp_server helpers
    if mcp_server is None:
        raise HTTPException(status_code=500, detail="Agent runtime not available")

    # Find event/company matches
    # Improved substring matching so NL queries still match event/company names
    events = mcp_server.query(
        "SELECT e.id, e.name, e.start_time, c.name as company_name FROM event e JOIN company c ON e.company_id = c.id WHERE ? LIKE '%' || e.name || '%'",
        (query,),
    )

    companies = mcp_server.query("SELECT id, name FROM company WHERE ? LIKE '%' || name || '%'", (query,))

    if not events and not companies:
        raise HTTPException(status_code=404, detail="No such events found")

    # Prefer first event match if present
    entity_id = None
    is_event = False
    if events:
        entity_id = events[0].get("id")
        is_event = True
    else:
        # If only a company matched, pick the first company's portfolio
        entity_id = companies[0].get("id")

    if is_event:
        kpis = mcp_server.get_event_kpis(entity_id)
        breakdown = mcp_server.get_event_emissions_breakdown(entity_id)
        # Fetch branding if available
        db_row = mcp_server.query("SELECT company_id FROM event WHERE id = ?", (entity_id,))
        branding = None
        if db_row and db_row[0].get("company_id"):
            branding = mcp_server.get_branding_config(db_row[0].get("company_id"))

        html = _build_html_report(kpis, breakdown, branding)
    else:
        # Company-level report
        summary = mcp_server.get_company_portfolio_summary(entity_id)
        monthly = mcp_server.get_company_monthly_emissions(entity_id, year=str(os.getenv("REPORT_YEAR", "2025")))
        branding = mcp_server.get_branding_config(entity_id)
        # Simple company HTML
        html = ["<html><body>", f"<h1>Company {summary.get('company_name','')}</h1>", "<h2>Summary</h2>", f"<pre>{summary}</pre>", "<h2>Monthly</h2>", f"<pre>{monthly}</pre>", f"<pre>branding: {branding}</pre>", "</body></html>"]
        html = "\n".join(html)

    # Save HTML to the reports dir (create if needed). If user supplied save_path
    # use that; otherwise create a unique filename in reports/.
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    fname = payload.save_path or f"reports/report_{uuid.uuid4().hex}.html"
    with open(fname, "w", encoding="utf-8") as fh:
        fh.write(html)

    # Return HTML directly as the response body for easy preview in clients
    return HTMLResponse(content=html)


def get_app() -> FastAPI:
    """Return the FastAPI app instance (useful for WSGI/ASGI servers)."""
    return app


if __name__ == "__main__":  # pragma: no cover - development runner
    import uvicorn

    uvicorn.run(get_app(), host="0.0.0.0", port=8000)
