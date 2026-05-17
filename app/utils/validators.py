"""
Input validators for form data and API inputs.

Provides real-time validation feedback for the UI layer.
"""

from __future__ import annotations

import re


def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format."""
    if not email:
        return False, "Email is required"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate phone number (flexible — allows international formats)."""
    if not phone:
        return False, "Phone number is required"
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    if not cleaned.isdigit() or len(cleaned) < 7 or len(cleaned) > 15:
        return False, "Invalid phone number"
    return True, ""


def validate_name(name: str) -> tuple[bool, str]:
    """Validate candidate name."""
    if not name or not name.strip():
        return False, "Name is required"
    if len(name.strip()) < 2:
        return False, "Name is too short"
    return True, ""


def validate_url(url: str) -> tuple[bool, str]:
    """Validate a URL (optional field)."""
    if not url:
        return True, ""  # Optional
    pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+$'
    if not re.match(pattern, url):
        return False, "Invalid URL format"
    return True, ""


def validate_job_description(jd: str) -> tuple[bool, str]:
    """Validate a job description for ATS analysis."""
    if not jd or not jd.strip():
        return False, "Job description is required for ATS analysis"
    if len(jd.strip()) < 50:
        return False, "Job description is too short for meaningful analysis (min 50 characters)"
    return True, ""


def get_field_status(is_valid: bool) -> str:
    """Return an emoji indicator for field validation status."""
    return "✅" if is_valid else "❌"
