
import sqlite3
from typing import List, Dict, Any

DB_PATH = "event_emissions.db"

def get_db_connection(path: str = None):
    """Establishes a database connection with row factory enabled."""
    p = path or DB_PATH
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql: str, params=()) -> List[Dict[str, Any]]:
    """Helper to run queries and return clean dictionaries."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()


def apply_ddl_and_mockdata(ddl_path: str = 'ddl.sql', mockdata_path: str = 'mockdata.sql', db_path: str = DB_PATH):
    """Run DDL + mockdata SQL files to produce a clean sqlite DB."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(open(ddl_path, 'r', encoding='utf-8').read())
    conn.commit()
    cur.executescript(open(mockdata_path, 'r', encoding='utf-8').read())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print('Creating DB using', DB_PATH)
    apply_ddl_and_mockdata()
