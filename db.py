import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_jobs (
                id          TEXT NOT NULL,
                source      TEXT NOT NULL,
                company     TEXT NOT NULL,
                title       TEXT NOT NULL,
                url         TEXT NOT NULL,
                location    TEXT,
                date_seen   TEXT NOT NULL,
                PRIMARY KEY (id, source)
            )
        """)


def has_seen(job_id: str, source: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_jobs WHERE id = ? AND source = ?",
            (job_id, source),
        ).fetchone()
    return row is not None


def upsert_job(job: dict) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO seen_jobs (id, source, company, title, url, location, date_seen)
            VALUES (:id, :source, :company, :title, :url, :location, :date_seen)
            ON CONFLICT (id, source) DO UPDATE SET
                title    = excluded.title,
                url      = excluded.url,
                location = excluded.location
            """,
            {**job, "date_seen": job.get("date_seen", date.today().isoformat())},
        )
