import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("data") / "ids.db"

def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                severity TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                src_ip TEXT NOT NULL,
                details TEXT
            )
            """
        )

def insert_event(ts: str, severity: str, alert_type: str, src_ip: str, details: str = "") -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO events (ts, severity, alert_type, src_ip, details)
            VALUES (?, ?, ?, ?, ?)
            """,
            (ts, severity, alert_type, src_ip, details),
        )
        return int(cur.lastrowid)

def get_latest_events(limit: int = 50) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, ts, severity, alert_type, src_ip, details
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

def seed_if_empty() -> None:
    with _connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM events").fetchone()
        count = int(row["c"]) if row else 0

    if count == 0:
        # Add sample events so the dashboard has something to show
        insert_event("2026-01-12 12:03:44", "HIGH", "Port Scan Detected", "192.168.1.23",
                     "Multiple ports targeted within a short time window.")
        insert_event("2026-01-12 12:01:10", "MED", "Suspicious DNS Query Rate", "192.168.1.11",
                     "High frequency of DNS queries observed.")
        insert_event("2026-01-12 11:57:05", "LOW", "New Device Seen", "192.168.1.58",
                     "Previously unseen device appeared on the network.")
