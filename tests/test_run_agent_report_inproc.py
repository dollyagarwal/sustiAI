import sys
import pathlib
import os
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from src.sustiai.api import app
from src.sustiai import mcp_server, db


def test_run_agent_report_inproc(tmp_path, monkeypatch):
    # Force the app to use the in-process MCP toolset (no stdio subprocess)
    monkeypatch.setenv("USE_INPROC_MCP", "1")

    # create a temporary DB and populate
    tmp_db = tmp_path / "tmp_report.db"
    db.apply_ddl_and_mockdata(db_path=str(tmp_db))
    mcp_server.DB_PATH = str(tmp_db)

    client = TestClient(app)
    payload = {"query": "Sustainability Summit Visionary Group"}
    r = client.post("/run_agent_report", json=payload)

    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("text/html")
    assert "Sustainability Summit" in r.text or "Visionary Group" in r.text
