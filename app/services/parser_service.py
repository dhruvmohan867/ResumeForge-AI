"""
Resume parsing service.

Extracts structured resume data from uploaded PDFs using:
1. PyPDF2 for text extraction
2. GPT-4o-mini for intelligent structured parsing
3. Pydantic validation for schema enforcement
"""

from __future__ import annotations

import io
from typing import Optional

from PyPDF2 import PdfReader

from app.config import AI_TEMPERATURE_LOW, MAX_TOKENS_PARSE
from app.models.resume_schema import (
    ResumeData,
    PersonalInfo,
    Education,
    WorkExperience,
    Project,
    Certification,
)
from app.services.ai_service import ai_service
from app.utils.constants import PROMPT_PARSE_RESUME
from app.utils.helpers import clean_text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract raw text content from a PDF file.
    
    Args:
        file_bytes: Raw bytes of the PDF file
        
    Returns:
        Extracted text as a single string
        
    Raises:
        ValueError: If the PDF is unreadable or empty
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))

        if len(reader.pages) == 0:
            raise ValueError("PDF has no pages")

        text_parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        full_text = "\n".join(text_parts)

        if not full_text.strip():
            raise ValueError(
                "Could not extract text from PDF. "
                "The file may be image-based or encrypted."
            )

        return clean_text(full_text)

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")


def parse_resume_with_ai(resume_text: str) -> ResumeData:
    """
    Use GPT-4o-mini to intelligently parse resume text into
    a structured ResumeData object.
    
    Args:
        resume_text: Raw text extracted from a resume PDF
        
    Returns:
        Validated ResumeData instance
    """
    prompt = PROMPT_PARSE_RESUME.format(resume_text=resume_text[:8000])

    parsed = ai_service.generate_json(
        system_prompt=(
            "You are a precise resume parser. "
            "Extract ALL information exactly as written. "
            "Return valid JSON only."
        ),
        user_prompt=prompt,
        temperature=AI_TEMPERATURE_LOW,
        max_tokens=MAX_TOKENS_PARSE,
    )

    return _build_resume_from_dict(parsed)


def parse_uploaded_pdf(file_bytes: bytes) -> ResumeData:
    """
    End-to-end pipeline: PDF bytes → text extraction → AI parsing → validated schema.
    
    Args:
        file_bytes: Raw bytes of the uploaded PDF
        
    Returns:
        Validated ResumeData instance
    """
    text = extract_text_from_pdf(file_bytes)
    return parse_resume_with_ai(text)


def _build_resume_from_dict(data: dict) -> ResumeData:
    """
    Safely build a ResumeData object from a parsed dictionary.
    Handles missing keys and malformed data gracefully.
    """
    try:
        personal = data.get("personal_info", {})
        personal_info = PersonalInfo(
            name=personal.get("name", ""),
            email=personal.get("email", ""),
            phone=personal.get("phone", ""),
            linkedin=personal.get("linkedin", ""),
            github=personal.get("github", ""),
            location=personal.get("location", ""),
            summary=personal.get("summary", ""),
        )

        education = [
            Education(
                degree=edu.get("degree", ""),
                institution=edu.get("institution", ""),
                year=edu.get("year", ""),
                gpa=edu.get("gpa", ""),
                highlights=edu.get("highlights", ""),
            )
            for edu in data.get("education", [])
            if isinstance(edu, dict)
        ]

        experience = [
            WorkExperience(
                job_title=exp.get("job_title", ""),
                company=exp.get("company", ""),
                duration=exp.get("duration", ""),
                description=exp.get("description", ""),
                location=exp.get("location", ""),
            )
            for exp in data.get("experience", [])
            if isinstance(exp, dict)
        ]

        skills = [
            s for s in data.get("skills", [])
            if isinstance(s, str) and s.strip()
        ]

        projects = [
            Project(
                title=proj.get("title", ""),
                technologies=proj.get("technologies", ""),
                description=proj.get("description", ""),
                link=proj.get("link", ""),
            )
            for proj in data.get("projects", [])
            if isinstance(proj, dict)
        ]

        certifications = [
            Certification(
                title=cert.get("title", ""),
                issuer=cert.get("issuer", ""),
                year=cert.get("year", ""),
            )
            for cert in data.get("certifications", [])
            if isinstance(cert, dict)
        ]

        return ResumeData(
            personal_info=personal_info,
            education=education,
            experience=experience,
            skills=skills,
            projects=projects,
            certifications=certifications,
        )

    except Exception as e:
        raise ValueError(f"Failed to build resume from parsed data: {str(e)}")
