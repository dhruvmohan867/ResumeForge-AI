"""
SQLite database layer for resume persistence.

Uses parameterized queries for security and provides
a clean interface for CRUD operations.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from typing import Optional

from app.config import DATABASE_PATH
from app.models.resume_schema import ResumeData


def _get_connection() -> sqlite3.Connection:
    """Create a database connection with row factory."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database schema if it doesn't exist."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                resume_json TEXT NOT NULL,
                completeness_score INTEGER DEFAULT 0,
                ats_score INTEGER,
                template_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_resume(resume_data: ResumeData, template: str = "") -> str:
    """
    Save or update a resume record.
    
    Returns the resume ID.
    """
    conn = _get_connection()
    try:
        resume_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO resumes 
               (id, name, email, phone, resume_json, completeness_score, template_used, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                resume_id,
                resume_data.personal_info.name,
                resume_data.personal_info.email,
                resume_data.personal_info.phone,
                resume_data.model_dump_json(),
                resume_data.completeness_score(),
                template,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        return resume_id
    finally:
        conn.close()


def get_recent_resumes(limit: int = 10) -> list[dict]:
    """Retrieve recent resume records."""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT id, name, email, completeness_score, created_at FROM resumes ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_resume_by_id(resume_id: str) -> Optional[ResumeData]:
    """Retrieve a full resume by ID."""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT resume_json FROM resumes WHERE id = ?", (resume_id,)
        ).fetchone()
        if row:
            return ResumeData.model_validate_json(row["resume_json"])
        return None
    finally:
        conn.close()
