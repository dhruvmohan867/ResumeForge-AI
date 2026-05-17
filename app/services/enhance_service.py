"""
AI Enhancement service for resume content improvement.

Provides XYZ formula bullet rewriting, summary optimization,
and project description enhancement using GPT-4o-mini.
"""

from __future__ import annotations

from app.config import AI_TEMPERATURE_MEDIUM, MAX_TOKENS_ENHANCE
from app.models.resume_schema import EnhancementResult
from app.services.ai_service import ai_service
from app.utils.constants import (
    PROMPT_ENHANCE_EXPERIENCE,
    PROMPT_ENHANCE_SUMMARY,
    PROMPT_ENHANCE_PROJECT,
)


def enhance_experience(
    original_text: str,
    job_title: str = "",
    company: str = "",
) -> EnhancementResult:
    """
    Enhance work experience bullets using Google's XYZ formula.
    
    Args:
        original_text: Original experience description
        job_title: Position title for context
        company: Company name for context
        
    Returns:
        EnhancementResult with improved text and change notes
    """
    if not original_text.strip():
        return EnhancementResult(
            original=original_text,
            enhanced=original_text,
            changes_made=[],
            improvement_notes="No content to enhance",
        )

    prompt = PROMPT_ENHANCE_EXPERIENCE.format(
        original_text=original_text,
        job_title=job_title or "Not specified",
        company=company or "Not specified",
    )

    result = ai_service.generate_json(
        system_prompt=(
            "You are a professional resume writer specializing in "
            "Google's XYZ formula and ATS optimization. "
            "Return valid JSON only."
        ),
        user_prompt=prompt,
        temperature=AI_TEMPERATURE_MEDIUM,
        max_tokens=MAX_TOKENS_ENHANCE,
    )

    return _build_enhancement(original_text, result)


def enhance_summary(
    original_text: str,
    skills: list[str] | None = None,
    target_role: str = "",
) -> EnhancementResult:
    """
    Enhance professional summary for ATS and impact.
    """
    if not original_text.strip():
        return EnhancementResult(
            original=original_text,
            enhanced=original_text,
            changes_made=[],
            improvement_notes="No content to enhance",
        )

    prompt = PROMPT_ENHANCE_SUMMARY.format(
        original_text=original_text,
        skills=", ".join(skills or []),
        target_role=target_role or "Software Engineer",
    )

    result = ai_service.generate_json(
        system_prompt=(
            "You are a professional resume writer. "
            "Return valid JSON only."
        ),
        user_prompt=prompt,
        temperature=AI_TEMPERATURE_MEDIUM,
        max_tokens=MAX_TOKENS_ENHANCE,
    )

    return _build_enhancement(original_text, result)


def enhance_project(
    original_text: str,
    project_title: str = "",
    technologies: str = "",
) -> EnhancementResult:
    """
    Enhance project description for technical impact.
    """
    if not original_text.strip():
        return EnhancementResult(
            original=original_text,
            enhanced=original_text,
            changes_made=[],
            improvement_notes="No content to enhance",
        )

    prompt = PROMPT_ENHANCE_PROJECT.format(
        original_text=original_text,
        project_title=project_title or "Not specified",
        technologies=technologies or "Not specified",
    )

    result = ai_service.generate_json(
        system_prompt=(
            "You are a technical resume writer. "
            "Return valid JSON only."
        ),
        user_prompt=prompt,
        temperature=AI_TEMPERATURE_MEDIUM,
        max_tokens=MAX_TOKENS_ENHANCE,
    )

    return _build_enhancement(original_text, result)


def _build_enhancement(original: str, data: dict) -> EnhancementResult:
    """Safely build an EnhancementResult from AI response."""
    try:
        return EnhancementResult(
            original=original,
            enhanced=data.get("enhanced", original),
            changes_made=data.get("changes_made", []),
            improvement_notes=data.get("improvement_notes", ""),
        )
    except Exception:
        return EnhancementResult(
            original=original,
            enhanced=original,
            changes_made=[],
            improvement_notes="Enhancement failed — original preserved.",
        )
