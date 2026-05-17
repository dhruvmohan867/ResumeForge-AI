"""
Utility helpers used across the application.

Contains reusable functions for text processing, file validation,
session state management, and common transformations.
"""

from __future__ import annotations

import json
import re
from typing import Any

import streamlit as st

from app.utils.constants import SESSION_TOAST_QUEUE


# ---------------------------------------------------------------------------
# Text Utilities
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Remove excessive whitespace and normalize line endings."""
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


def extract_json_from_response(text: str) -> dict[str, Any]:
    """
    Extract JSON from an AI response that may contain markdown fences or
    extra text surrounding the JSON block.
    """
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code fences
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding the first { ... } block
    brace_match = re.search(r'\{.*\}', text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from AI response")


def skills_to_list(skills_string: str) -> list[str]:
    """Convert comma-separated skills string to a clean list."""
    if not skills_string:
        return []
    return [s.strip() for s in skills_string.split(",") if s.strip()]


def skills_to_string(skills_list: list[str]) -> str:
    """Convert skills list back to comma-separated string."""
    return ", ".join(skills_list)


# ---------------------------------------------------------------------------
# File Validation
# ---------------------------------------------------------------------------

def validate_pdf_upload(uploaded_file) -> tuple[bool, str]:
    """
    Validate an uploaded PDF file.
    
    Returns:
        (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"

    # Check file type
    if uploaded_file.type != "application/pdf":
        return False, "Only PDF files are accepted"

    # Check file size (5 MB limit)
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 5:
        return False, f"File too large ({file_size_mb:.1f} MB). Maximum is 5 MB."

    return True, ""


# ---------------------------------------------------------------------------
# Session State Helpers
# ---------------------------------------------------------------------------

def init_session_state(key: str, default: Any) -> None:
    """Initialize a session state key if it doesn't exist."""
    if key not in st.session_state:
        st.session_state[key] = default


def get_session(key: str, default: Any = None) -> Any:
    """Safely retrieve a session state value."""
    return st.session_state.get(key, default)


def set_session(key: str, value: Any) -> None:
    """Set a session state value."""
    st.session_state[key] = value


def queue_toast(message: str, icon: str = "✅") -> None:
    """Queue a toast notification to be shown on next rerun."""
    if SESSION_TOAST_QUEUE not in st.session_state:
        st.session_state[SESSION_TOAST_QUEUE] = []
    st.session_state[SESSION_TOAST_QUEUE].append({"message": message, "icon": icon})


def flush_toasts() -> None:
    """Display and clear all queued toast notifications."""
    toasts = st.session_state.get(SESSION_TOAST_QUEUE, [])
    for t in toasts:
        st.toast(t["message"], icon=t["icon"])
    st.session_state[SESSION_TOAST_QUEUE] = []


# ---------------------------------------------------------------------------
# Formatting Helpers
# ---------------------------------------------------------------------------

def format_score_color(score: int) -> str:
    """Return a CSS color based on score value."""
    if score >= 80:
        return "#10b981"   # Green
    elif score >= 60:
        return "#f59e0b"   # Amber
    elif score >= 40:
        return "#f97316"   # Orange
    else:
        return "#ef4444"   # Red


def format_score_label(score: int) -> str:
    """Return a human-readable label for a score."""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Needs Improvement"
    else:
        return "Weak"
