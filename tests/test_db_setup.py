
import os
import tempfile
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.sustiai import db


def test_apply_ddl_and_mockdata_creates_db():
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    tmp_db = tmp_file.name
    tmp_file.close()

    try:
        # Create DB using the shipped SQL files (assumes they exist in cwd)
        db.apply_ddl_and_mockdata(ddl_path='ddl.sql', mockdata_path='mockdata.sql', db_path=tmp_db)
        conn = db.get_db_connection(path=tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='event';")
        row = cur.fetchone()
        assert row is not None and row[0] == 'event'
        conn.close()
    finally:
        os.unlink(tmp_db)
