import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.sustiai.api import app
from src.sustiai.db import apply_ddl_and_mockdata
from src.sustiai import mcp_server


def test_run_agent_report_endpoint(tmp_path):
    tmp_db = tmp_path / "tmp_report.db"
    apply_ddl_and_mockdata(db_path=str(tmp_db))

    # ensure mcp_server uses the new DB
    mcp_server.DB_PATH = str(tmp_db)

    client = TestClient(app)

    payload = {"query": "Give me a detailed carbon accounting report for Sustainability Summit event of Visionary Group"}
    r = client.post("/run_agent_report", json=payload)
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/html")
    assert "Sustainability Summit" in r.text or "Visionary Group" in r.text
