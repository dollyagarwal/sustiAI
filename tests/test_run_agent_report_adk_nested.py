import sys
import pathlib
import pytest
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.sustiai.api import app


def test_run_agent_report_endpoint_adk_state_html(monkeypatch):
    """Simulate a complex ADK response with nested state_delta containing the
    HTML report (string). The endpoint should find and return the HTML.
    """

    html = "<!DOCTYPE html><html><body><h1>NESTED_HTML_REPORT</h1></body></html>"

    class FakeRunner:
        class FakeSessionService:
            async def create_session(self, app_name=None, user_id=None):
                class S: pass
                s = S()
                s.id = "fake-session"
                return s

        session_service = FakeSessionService()

        async def run_debug(self, *args, **kwargs):
            # return a nested structure similar to what ADK may produce
            return {"events": [{"actions": {"state_delta": {"report": html}}}]}

    import src.sustiai.agents.orchestrator as orchestrator

    monkeypatch.setattr(orchestrator, "HAS_ADK", True)
    monkeypatch.setattr(orchestrator, "runner", FakeRunner())

    client = TestClient(app)
    payload = {"query": "any query"}
    r = client.post("/run_agent_report", json=payload)

    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/html")
    assert "NESTED_HTML_REPORT" in r.text


def test_run_agent_report_endpoint_adk_saved_path(monkeypatch, tmp_path):
    """Simulate ADK response that references a saved file under reports/.
    The endpoint should detect the filepath and return the file contents.
    """

    reports_dir = pathlib.Path("reports")
    reports_dir.mkdir(exist_ok=True)
    saved_file = reports_dir / "EcoSphere Ltd.html"
    html = "<!DOCTYPE html><html><body><h1>SAVED_FILE_REPORT</h1></body></html>"
    saved_file.write_text(html, encoding="utf-8")

    class FakeRunner2:
        class FakeSessionService:
            async def create_session(self, app_name=None, user_id=None):
                class S: pass
                s = S()
                s.id = "fake-session"
                return s

        session_service = FakeSessionService()

        async def run_debug(self, *args, **kwargs):
            # ADK might return a string mentioning where the report was saved
            # Simulate a string with a space-containing path as some agents save
            # reports using the company name with spaces (e.g. 'EcoSphere Ltd').
            return {"message": f"Saved report to {str(saved_file.parent / 'EcoSphere Ltd.html')}"}

    import src.sustiai.agents.orchestrator as orchestrator

    monkeypatch.setattr(orchestrator, "HAS_ADK", True)
    monkeypatch.setattr(orchestrator, "runner", FakeRunner2())

    client = TestClient(app)
    payload = {"query": "any query"}
    r = client.post("/run_agent_report", json=payload)

    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/html")
    assert "SAVED_FILE_REPORT" in r.text
