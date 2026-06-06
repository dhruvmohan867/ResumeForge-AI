"""
Application-wide constants and prompt templates.

Centralizes all magic strings, prompt templates, and
configuration constants used across services.
"""

# ---------------------------------------------------------------------------
# Session State Keys
# ---------------------------------------------------------------------------
SESSION_RESUME_DATA = "resume_data"
SESSION_ATS_RESULT = "ats_result"
SESSION_JOB_DESCRIPTION = "job_description"
SESSION_SELECTED_TEMPLATE = "selected_template"
SESSION_ACTIVE_TAB = "active_tab"
SESSION_PARSED_RESUME = "parsed_resume"
SESSION_DARK_MODE = "dark_mode"
SESSION_TOAST_QUEUE = "toast_queue"

# ---------------------------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------------------------
NAV_TABS = [
    ("📝", "Resume Builder"),
    ("📄", "Upload & Parse"),
    ("🎯", "ATS Analysis"),
    ("✨", "AI Enhance"),
    ("✉️", "Cover Letter"),
    ("📥", "Export PDF"),
]

# ---------------------------------------------------------------------------
# AI Prompt Templates
# ---------------------------------------------------------------------------

PROMPT_PARSE_RESUME = """You are an expert resume parser. Extract ALL information from the following resume text into a structured JSON format.

Be thorough and extract every detail. If a field is not found, use an empty string.

Resume Text:
---
{resume_text}
---

Return ONLY valid JSON matching this exact structure:
{{
    "personal_info": {{
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "location": "",
        "summary": ""
    }},
    "education": [
        {{
            "degree": "",
            "institution": "",
            "year": "",
            "gpa": "",
            "highlights": ""
        }}
    ],
    "experience": [
        {{
            "job_title": "",
            "company": "",
            "duration": "",
            "description": "",
            "location": ""
        }}
    ],
    "skills": ["skill1", "skill2"],
    "projects": [
        {{
            "title": "",
            "technologies": "",
            "description": "",
            "link": ""
        }}
    ],
    "certifications": [
        {{
            "title": "",
            "issuer": "",
            "year": ""
        }}
    ]
}}"""

PROMPT_ATS_ANALYSIS = """You are an expert ATS (Applicant Tracking System) analyzer. 
Analyze the following resume against the provided job description.

RESUME DATA:
{resume_json}

JOB DESCRIPTION:
{job_description}

Perform a thorough ATS compatibility analysis and return ONLY valid JSON:
{{
    "overall_score": <0-100>,
    "keyword_score": <0-100>,
    "experience_relevance": <0-100>,
    "skills_match": <0-100>,
    "formatting_score": <0-100>,
    "matched_keywords": ["keyword1", "keyword2"],
    "missing_keywords": ["keyword1", "keyword2"],
    "missing_skills": ["skill1", "skill2"],
    "missing_soft_skills": ["skill1", "skill2"],
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2"
    ],
    "summary": "Brief overall assessment"
}}

Scoring Guidelines:
- keyword_score: % of important JD keywords found in resume
- experience_relevance: How well experience aligns with JD requirements
- skills_match: % of required skills present in resume
- formatting_score: Resume structure quality for ATS parsing
- overall_score: Weighted average (keywords 30%, experience 30%, skills 25%, formatting 15%)

Be realistic and specific. Do not inflate scores."""

PROMPT_ENHANCE_EXPERIENCE = """You are a professional resume writer specializing in Google's XYZ formula.

Rewrite the following work experience bullet points to be more impactful.

Original:
{original_text}

Context:
- Job Title: {job_title}
- Company: {company}

Rules:
1. Use Google's XYZ Formula: "Accomplished [X] as measured by [Y], by doing [Z]"
2. Start each bullet with a strong action verb
3. Include quantifiable metrics where possible (use realistic estimates if none given)
4. Keep it concise — max 2 lines per bullet
5. Maintain professional tone and factual accuracy
6. Do NOT fabricate achievements — enhance what exists

Return ONLY valid JSON:
{{
    "enhanced": "The rewritten text with bullet points",
    "changes_made": ["List of specific changes made"],
    "improvement_notes": "Brief explanation of improvements"
}}"""

PROMPT_ENHANCE_SUMMARY = """You are a professional resume writer.

Rewrite the following professional summary to be more compelling and ATS-friendly.

Original Summary:
{original_text}

Candidate Skills: {skills}
Target Role: {target_role}

Rules:
1. Keep to 3-4 sentences maximum
2. Include relevant keywords naturally
3. Highlight unique value proposition
4. Use confident, professional tone
5. Avoid clichés like "hard-working" or "team player"
6. Focus on measurable impact and domain expertise

Return ONLY valid JSON:
{{
    "enhanced": "The rewritten summary",
    "changes_made": ["List of specific changes"],
    "improvement_notes": "Brief explanation"
}}"""

PROMPT_ENHANCE_PROJECT = """You are a professional resume writer.

Rewrite the following project description to be more impactful for a technical resume.

Original:
{original_text}

Project Title: {project_title}
Technologies: {technologies}

Rules:
1. Lead with the problem solved or impact created
2. Mention technologies naturally within the description
3. Include scale/metrics if possible
4. Keep to 2-3 concise bullet points
5. Use strong technical action verbs

Return ONLY valid JSON:
{{
    "enhanced": "The rewritten project description",
    "changes_made": ["List of specific changes"],
    "improvement_notes": "Brief explanation"
}}"""

# ---------------------------------------------------------------------------
# PDF Template Constants
# ---------------------------------------------------------------------------
PDF_MARGIN_LEFT = 15
PDF_MARGIN_RIGHT = 15
PDF_MARGIN_TOP = 15
PDF_PAGE_WIDTH = 210  # A4
PDF_CONTENT_WIDTH = PDF_PAGE_WIDTH - PDF_MARGIN_LEFT - PDF_MARGIN_RIGHT

# Color Palettes for Templates
TEMPLATE_COLORS = {
    "tech_minimalist": {
        "primary": (41, 98, 255),       # Blue
        "secondary": (100, 116, 139),   # Slate
        "accent": (16, 185, 129),       # Emerald
        "text": (30, 41, 59),           # Dark
        "light": (241, 245, 249),       # Light bg
    },
    "corporate_executive": {
        "primary": (30, 41, 59),        # Navy
        "secondary": (71, 85, 105),     # Gray
        "accent": (180, 142, 87),       # Gold
        "text": (30, 41, 59),           # Dark
        "light": (248, 250, 252),       # Light bg
    },
    "modern_developer": {
        "primary": (124, 58, 237),      # Purple
        "secondary": (100, 116, 139),   # Slate
        "accent": (236, 72, 153),       # Pink
        "text": (30, 41, 59),           # Dark
        "light": (245, 243, 255),       # Light bg
    },
}
