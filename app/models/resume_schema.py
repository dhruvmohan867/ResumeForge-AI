"""
Pydantic schemas for resume data validation.

All AI structured outputs and form data are validated through
these models before being used in any service layer.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Core Resume Data Models
# ---------------------------------------------------------------------------

class PersonalInfo(BaseModel):
    """Contact and identity information."""
    name: str = Field(default="", description="Full name of the candidate")
    email: str = Field(default="", description="Email address")
    phone: str = Field(default="", description="Phone number")
    linkedin: str = Field(default="", description="LinkedIn profile URL")
    github: str = Field(default="", description="GitHub profile URL")
    location: str = Field(default="", description="City, State/Country")
    summary: str = Field(default="", description="Professional summary / objective")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v.strip()

    @field_validator("name", "phone", "linkedin", "github", "location", "summary")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class Education(BaseModel):
    """Single education entry."""
    degree: str = Field(default="", description="Degree title (e.g. B.Tech in CSE)")
    institution: str = Field(default="", description="University / college name")
    year: str = Field(default="", description="Graduation year or range")
    gpa: str = Field(default="", description="GPA or percentage")
    highlights: str = Field(default="", description="Coursework, honors, etc.")


class WorkExperience(BaseModel):
    """Single work experience entry."""
    job_title: str = Field(default="", description="Position / role title")
    company: str = Field(default="", description="Company name")
    duration: str = Field(default="", description="Date range (e.g. Jan 2024 – Present)")
    description: str = Field(default="", description="Bullet points describing the role")
    location: str = Field(default="", description="City, Country")


class Project(BaseModel):
    """Single project entry."""
    title: str = Field(default="", description="Project title")
    technologies: str = Field(default="", description="Tech stack used")
    description: str = Field(default="", description="Project description and impact")
    link: str = Field(default="", description="GitHub/live link")


class Certification(BaseModel):
    """Single certification entry."""
    title: str = Field(default="", description="Certification name")
    issuer: str = Field(default="", description="Issuing organization")
    year: str = Field(default="", description="Year obtained")


# ---------------------------------------------------------------------------
# Complete Resume Data Envelope
# ---------------------------------------------------------------------------

class ResumeData(BaseModel):
    """
    Complete resume data model.
    
    This is the central schema that flows through every service:
    - AI parser outputs this shape
    - Form state maps to/from this shape
    - PDF engine consumes this shape
    - ATS engine analyzes this shape
    """
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    education: list[Education] = Field(default_factory=list)
    experience: list[WorkExperience] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list, description="List of skills")
    projects: list[Project] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if the resume has any meaningful content."""
        return (
            not self.personal_info.name
            and not self.education
            and not self.experience
            and not self.skills
            and not self.projects
        )

    def completeness_score(self) -> int:
        """Return a 0-100 completeness percentage."""
        score = 0
        # Personal info (20 points)
        if self.personal_info.name:
            score += 5
        if self.personal_info.email:
            score += 5
        if self.personal_info.phone:
            score += 3
        if self.personal_info.summary:
            score += 7
        # Education (15 points)
        if self.education:
            score += 15
        # Experience (25 points)
        if self.experience:
            score += min(25, len(self.experience) * 10)
        # Skills (20 points)
        if self.skills:
            score += min(20, len(self.skills) * 2)
        # Projects (15 points)
        if self.projects:
            score += min(15, len(self.projects) * 5)
        # Certifications (5 points)
        if self.certifications:
            score += 5
        return min(score, 100)


# ---------------------------------------------------------------------------
# ATS Analysis Result
# ---------------------------------------------------------------------------

class KeywordMatch(BaseModel):
    """Single keyword match detail."""
    keyword: str
    found: bool
    context: str = Field(default="", description="Where the keyword was found")


class ATSResult(BaseModel):
    """ATS analysis output."""
    overall_score: int = Field(ge=0, le=100, description="ATS match percentage")
    keyword_score: int = Field(ge=0, le=100)
    experience_relevance: int = Field(ge=0, le=100)
    skills_match: int = Field(ge=0, le=100)
    formatting_score: int = Field(ge=0, le=100)
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    missing_soft_skills: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    summary: str = Field(default="")


# ---------------------------------------------------------------------------
# AI Enhancement Result
# ---------------------------------------------------------------------------

class EnhancementResult(BaseModel):
    """Result from AI content enhancement."""
    original: str
    enhanced: str
    changes_made: list[str] = Field(default_factory=list)
    improvement_notes: str = Field(default="")
