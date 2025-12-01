import sys
import pathlib
import tempfile
import os

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.sustiai.mcp_tool_local import LocalMCPToolset
from src.sustiai import db


def test_local_mcp_calls(tmp_path):
    # create a temporary DB and populate
    tmp_db = tmp_path / "tmp.db"
    db.apply_ddl_and_mockdata(db_path=str(tmp_db))

    # instruct the mcp_server to point to our tmp DB
    from src.sustiai import mcp_server

    mcp_server.DB_PATH = str(tmp_db)

    t = LocalMCPToolset()

    # describe_database should return SQL statements
    descr = t.describe_database()
    assert "CREATE TABLE" in descr

    # search_entities should return companies and events
    res = t.search_entities("Sustainability")
    assert isinstance(res, dict)
    assert "events" in res
