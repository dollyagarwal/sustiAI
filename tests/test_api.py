import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

# If FastAPI isn't installed in this environment, skip the API tests. The
# package still exposes the app module but running tests with the real
# fastapi/testclient requires the dependency.
pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.sustiai.api import app
from src.sustiai.db import apply_ddl_and_mockdata


def test_api_health_and_event_kpis(tmp_path):
    # create DB in a temporary path for isolation (don't clobber any local DB)
    tmp_db = tmp_path / "tmp_event_emissions.db"
    apply_ddl_and_mockdata(
        ddl_path="ddl.sql",
        mockdata_path="mockdata.sql",
        db_path=str(tmp_db),
    )

    # ensure the app uses the same DB path for the test (module-level DB_PATH)
    # patching module-level DB_PATH in the API's server helpers keeps this test
    # self-contained.
    from src.sustiai import mcp_server
    mcp_server.DB_PATH = str(tmp_db)

    client = TestClient(app)

    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"

    # event_id 1 should exist in the shipped mockdata
    r2 = client.get("/events/1/kpis")
    assert r2.status_code == 200
    assert "event_name" in r2.json()
