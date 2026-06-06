"""
AI-powered Cover Letter generation service.
"""

from __future__ import annotations

import json
from typing import Any

from app.models.resume_schema import ResumeData
from app.services.ai_service import ai_service


def generate_cover_letter(
    resume_data: ResumeData,
    job_description: str,
    tone: str = "Professional",
) -> dict[str, Any]:
    """
    Generate a tailored cover letter using AI based on resume and job description.
    
    Args:
        resume_data: Resume data model
        job_description: Job description text
        tone: Desired tone (e.g. Professional, Enthusiastic, Creative, Bold)
        
    Returns:
        A dictionary containing 'cover_letter' and 'hiring_manager_notes'
    """
    # Convert resume data to dictionary/JSON for LLM consumption
    resume_dict = {
        "personal_info": {
            "name": resume_data.personal_info.name,
            "email": resume_data.personal_info.email,
            "phone": resume_data.personal_info.phone,
            "location": resume_data.personal_info.location,
            "summary": resume_data.personal_info.summary,
        },
        "education": [
            {
                "degree": edu.degree,
                "institution": edu.institution,
                "year": edu.year,
            }
            for edu in resume_data.education
        ],
        "experience": [
            {
                "job_title": exp.job_title,
                "company": exp.company,
                "duration": exp.duration,
                "description": exp.description,
            }
            for exp in resume_data.experience
        ],
        "skills": resume_data.skills,
        "projects": [
            {
                "title": proj.title,
                "technologies": proj.technologies,
                "description": proj.description,
            }
            for proj in resume_data.projects
        ],
    }

    resume_json = json.dumps(resume_dict, indent=2)

    prompt = f"""You are an expert executive career coach and professional writer. 
Write a highly targeted, persuasive cover letter matching the candidate's resume details to the target job description.

Candidate Resume Data (JSON):
{resume_json}

Target Job Description:
{job_description}

Tone / Writing Style:
{tone}

Rules for the Cover Letter:
1. Ensure the cover letter is structured professionally with:
   - Header (Date, Candidate contact info placeholder, hiring manager salutation if appropriate)
   - Opening hook referencing the target role
   - Body paragraphs linking candidate achievements (using numbers/impact) directly to job description needs
   - Closing paragraph with call to action
2. Adapt the language to match the requested tone:
   - Professional: Formal, objective, authoritative.
   - Enthusiastic: High-energy, warm, deeply excited about the company's mission.
   - Creative: Narrative-driven, conversational, unique hook.
   - Bold: Confident, direct, highlights major achievements aggressively.
3. Keep it within 300-400 words (single page).
4. Do NOT fabricate skills or experiences. Only use facts present in the resume.

Return ONLY valid JSON with this exact structure:
{{
    "cover_letter": "The full text of the cover letter with newlines",
    "hiring_manager_notes": "A brief explanation of how this cover letter aligns with the job requirements and what parts were emphasized."
}}"""

    res = ai_service.generate_json(
        system_prompt="You are a professional resume writer and recruitment specialist.",
        user_prompt=prompt,
    )
    return res
