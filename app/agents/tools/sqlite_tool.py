import sqlite3
from typing import Any, Dict
from ...config import SQLITE_DB
def run_sql(query: str) -> Dict[str, Any]:
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cur = conn.cursor()
        cur.execute(query)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return {"columns": cols, "rows": rows, "rowcount": len(rows)}
    except Exception as e:
        return {"error": str(e)}
