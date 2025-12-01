import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.sustiai.api import app


def test_run_agent_report_endpoint_adk(monkeypatch):
    """Simulate an ADK orchestrator runner that produces HTML and ensure
    the endpoint returns the HTML content rather than the raw object dump.
    """

    # Create a fake orchestrator runner with session_service and run_debug
    class FakeSession:
        def __init__(self):
            self.id = "fake-session-id"

    class FakeSessionService:
        async def create_session(self, app_name=None, user_id=None):
            return FakeSession()

    class FakeRunner:
        session_service = FakeSessionService()

        async def run_debug(self, query, session_id=None, verbose=False):
            # Return a payload whose string contains HTML so the API extractor
            # will find it and return it as HTMLResponse
            return "<!DOCTYPE html><html><body><h1>FAKE_ADK_REPORT</h1></body></html>"

    # Monkeypatch the orchestrator module used by the endpoint
    import src.sustiai.agents.orchestrator as orchestrator

    monkeypatch.setattr(orchestrator, "HAS_ADK", True)
    monkeypatch.setattr(orchestrator, "runner", FakeRunner())

    client = TestClient(app)

    payload = {"query": "Produce a report for Sustainability Summit Visionary Group"}
    r = client.post("/run_agent_report", json=payload)

    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/html")
    assert "FAKE_ADK_REPORT" in r.text
