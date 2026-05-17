"""
ATS (Applicant Tracking System) analysis service.

Provides semantic job description matching, keyword gap analysis,
and actionable improvement suggestions using GPT-4o-mini.
"""

from __future__ import annotations

from app.config import AI_TEMPERATURE_LOW, MAX_TOKENS_ATS
from app.models.resume_schema import ResumeData, ATSResult
from app.services.ai_service import ai_service
from app.utils.constants import PROMPT_ATS_ANALYSIS


def analyze_ats_match(resume: ResumeData, job_description: str) -> ATSResult:
    """
    Perform comprehensive ATS analysis of a resume against a job description.
    
    Args:
        resume: The candidate's resume data
        job_description: Target job description text
        
    Returns:
        ATSResult with scores, matches, gaps, and suggestions
    """
    resume_json = resume.model_dump_json(indent=2)

    prompt = PROMPT_ATS_ANALYSIS.format(
        resume_json=resume_json[:6000],
        job_description=job_description[:4000],
    )

    result = ai_service.generate_json(
        system_prompt=(
            "You are an expert ATS system analyzer. "
            "Provide accurate, realistic scoring and actionable suggestions. "
            "Never inflate scores. Return valid JSON only."
        ),
        user_prompt=prompt,
        temperature=AI_TEMPERATURE_LOW,
        max_tokens=MAX_TOKENS_ATS,
    )

    return _build_ats_result(result)


def quick_score(resume: ResumeData) -> int:
    """
    Calculate a quick local completeness/quality score without AI.
    Used for instant feedback before full ATS analysis.
    
    Returns:
        Score from 0-100
    """
    score = 0

    # Personal info (20 points)
    pi = resume.personal_info
    if pi.name:
        score += 5
    if pi.email:
        score += 5
    if pi.phone:
        score += 3
    if pi.summary and len(pi.summary) > 30:
        score += 7

    # Education (15 points)
    if resume.education:
        score += 10
        if any(e.gpa for e in resume.education):
            score += 5

    # Experience (30 points)
    if resume.experience:
        exp_score = min(15, len(resume.experience) * 5)
        score += exp_score
        # Bonus for detailed descriptions
        desc_lengths = [len(e.description) for e in resume.experience]
        if desc_lengths and sum(desc_lengths) / len(desc_lengths) > 100:
            score += 10
        elif desc_lengths and sum(desc_lengths) / len(desc_lengths) > 50:
            score += 5

    # Skills (20 points)
    if resume.skills:
        score += min(20, len(resume.skills) * 2)

    # Projects (10 points)
    if resume.projects:
        score += min(10, len(resume.projects) * 3)

    # Certifications (5 points)
    if resume.certifications:
        score += 5

    return min(score, 100)


def _build_ats_result(data: dict) -> ATSResult:
    """Safely build an ATSResult from AI response dictionary."""
    try:
        return ATSResult(
            overall_score=_clamp(data.get("overall_score", 0)),
            keyword_score=_clamp(data.get("keyword_score", 0)),
            experience_relevance=_clamp(data.get("experience_relevance", 0)),
            skills_match=_clamp(data.get("skills_match", 0)),
            formatting_score=_clamp(data.get("formatting_score", 0)),
            matched_keywords=data.get("matched_keywords", []),
            missing_keywords=data.get("missing_keywords", []),
            missing_skills=data.get("missing_skills", []),
            missing_soft_skills=data.get("missing_soft_skills", []),
            suggestions=data.get("suggestions", []),
            summary=data.get("summary", ""),
        )
    except Exception:
        return ATSResult(
            overall_score=0,
            keyword_score=0,
            experience_relevance=0,
            skills_match=0,
            formatting_score=0,
            summary="ATS analysis could not be completed. Please try again.",
        )


def _clamp(value: int | float, low: int = 0, high: int = 100) -> int:
    """Clamp a numeric value to [low, high] range."""
    try:
        return max(low, min(high, int(value)))
    except (TypeError, ValueError):
        return 0
