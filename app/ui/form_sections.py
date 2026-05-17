"""
Resume builder form sections.

Each function renders a section of the resume builder form,
reading from and writing to st.session_state through the 
ResumeData model. All inputs are decoupled from forms to
prevent state reset issues.
"""

from __future__ import annotations

import streamlit as st

from app.models.resume_schema import (
    ResumeData,
    PersonalInfo,
    Education,
    WorkExperience,
    Project,
    Certification,
)
from app.utils.constants import SESSION_RESUME_DATA
from app.utils.helpers import get_session, set_session, skills_to_string, skills_to_list
from app.ui.components import render_section_header


def _get_resume() -> ResumeData:
    """Get current resume data from session state."""
    data = get_session(SESSION_RESUME_DATA)
    if data is None or not isinstance(data, ResumeData):
        data = ResumeData()
        set_session(SESSION_RESUME_DATA, data)
    return data


def _save_resume(data: ResumeData) -> None:
    """Save resume data back to session state."""
    set_session(SESSION_RESUME_DATA, data)


def render_personal_info_section() -> None:
    """Render the personal information form section."""
    render_section_header("👤", "Personal Information", "Your contact details and professional identity")

    resume = _get_resume()
    pi = resume.personal_info

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", value=pi.name, key="inp_name", placeholder="John Doe")
        email = st.text_input("Email Address *", value=pi.email, key="inp_email", placeholder="john@example.com")
        phone = st.text_input("Phone Number *", value=pi.phone, key="inp_phone", placeholder="+1 (555) 123-4567")
    with col2:
        location = st.text_input("Location", value=pi.location, key="inp_location", placeholder="San Francisco, CA")
        linkedin = st.text_input("LinkedIn URL", value=pi.linkedin, key="inp_linkedin", placeholder="https://linkedin.com/in/johndoe")
        github = st.text_input("GitHub URL", value=pi.github, key="inp_github", placeholder="https://github.com/johndoe")

    summary = st.text_area(
        "Professional Summary",
        value=pi.summary,
        key="inp_summary",
        height=100,
        placeholder="Experienced software engineer with 3+ years in full-stack development...",
    )

    # Update model
    resume.personal_info = PersonalInfo(
        name=name, email=email, phone=phone,
        location=location, linkedin=linkedin, github=github,
        summary=summary,
    )
    _save_resume(resume)


def render_education_section() -> None:
    """Render the education form section with dynamic entries."""
    render_section_header("🎓", "Education", "Your academic background")

    resume = _get_resume()

    # Ensure at least one entry
    if not resume.education:
        resume.education = [Education()]
        _save_resume(resume)

    updated_education: list[Education] = []

    for i, edu in enumerate(resume.education):
        with st.container():
            st.markdown(f"<p style='font-size:0.8rem; font-weight:600; color:var(--accent-color,#6366f1);'>Entry {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                degree = st.text_input("Degree", value=edu.degree, key=f"edu_degree_{i}", placeholder="B.Tech in Computer Science")
                institution = st.text_input("Institution", value=edu.institution, key=f"edu_inst_{i}", placeholder="MIT")
            with col2:
                year = st.text_input("Year", value=edu.year, key=f"edu_year_{i}", placeholder="2020 - 2024")
                gpa = st.text_input("GPA / Score", value=edu.gpa, key=f"edu_gpa_{i}", placeholder="3.8 / 4.0")
            highlights = st.text_input("Highlights", value=edu.highlights, key=f"edu_hl_{i}", placeholder="Dean's List, Relevant coursework...")

            updated_education.append(Education(
                degree=degree, institution=institution,
                year=year, gpa=gpa, highlights=highlights,
            ))

            if i < len(resume.education) - 1:
                st.markdown("<hr style='border-color:var(--border-color,rgba(255,255,255,0.06)); margin:0.5rem 0;'>", unsafe_allow_html=True)

    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Education", key="add_edu", use_container_width=True):
            updated_education.append(Education())
    with col_remove:
        if len(updated_education) > 1 and st.button("🗑️ Remove Last", key="rm_edu", use_container_width=True):
            updated_education.pop()

    resume.education = updated_education
    _save_resume(resume)


def render_experience_section() -> None:
    """Render work experience form section with dynamic entries."""
    render_section_header("💼", "Work Experience", "Your professional history")

    resume = _get_resume()

    if not resume.experience:
        resume.experience = [WorkExperience()]
        _save_resume(resume)

    updated_experience: list[WorkExperience] = []

    for i, exp in enumerate(resume.experience):
        with st.container():
            st.markdown(f"<p style='font-size:0.8rem; font-weight:600; color:var(--accent-color,#6366f1);'>Position {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Job Title", value=exp.job_title, key=f"exp_title_{i}", placeholder="Software Engineer")
                company = st.text_input("Company", value=exp.company, key=f"exp_company_{i}", placeholder="Google")
            with col2:
                duration = st.text_input("Duration", value=exp.duration, key=f"exp_dur_{i}", placeholder="Jan 2023 - Present")
                location = st.text_input("Location", value=exp.location, key=f"exp_loc_{i}", placeholder="Mountain View, CA")

            description = st.text_area(
                "Description (bullet points)",
                value=exp.description,
                key=f"exp_desc_{i}",
                height=120,
                placeholder="• Led development of microservices handling 10K+ RPM\n• Reduced API latency by 40% through query optimization",
            )

            updated_experience.append(WorkExperience(
                job_title=job_title, company=company,
                duration=duration, description=description,
                location=location,
            ))

            if i < len(resume.experience) - 1:
                st.markdown("<hr style='border-color:var(--border-color,rgba(255,255,255,0.06)); margin:0.5rem 0;'>", unsafe_allow_html=True)

    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Experience", key="add_exp", use_container_width=True):
            updated_experience.append(WorkExperience())
    with col_remove:
        if len(updated_experience) > 1 and st.button("🗑️ Remove Last", key="rm_exp", use_container_width=True):
            updated_experience.pop()

    resume.experience = updated_experience
    _save_resume(resume)


def render_skills_section() -> None:
    """Render skills input section."""
    render_section_header("🛠️", "Skills", "Your technical and professional skills")

    resume = _get_resume()
    current_skills = skills_to_string(resume.skills)

    skills_input = st.text_area(
        "Skills (comma-separated)",
        value=current_skills,
        key="inp_skills",
        height=80,
        placeholder="Python, JavaScript, React, Node.js, AWS, Docker, Git, SQL, Machine Learning",
    )

    resume.skills = skills_to_list(skills_input)
    _save_resume(resume)

    # Preview tags
    if resume.skills:
        st.markdown("<p style='font-size:0.75rem; color:var(--text-muted,#64748b); margin-top:0.5rem;'>Preview:</p>", unsafe_allow_html=True)
        tags_html = " ".join([
            f"<span style='display:inline-block; padding:0.2rem 0.6rem; margin:0.1rem; "
            f"border-radius:8px; font-size:0.75rem; background:rgba(99,102,241,0.15); "
            f"color:#818cf8; border:1px solid rgba(99,102,241,0.25);'>{s}</span>"
            for s in resume.skills
        ])
        st.markdown(f"<div style='line-height:2;'>{tags_html}</div>", unsafe_allow_html=True)


def render_projects_section() -> None:
    """Render projects form section with dynamic entries."""
    render_section_header("🚀", "Projects", "Showcase your best work")

    resume = _get_resume()

    if not resume.projects:
        resume.projects = [Project()]
        _save_resume(resume)

    updated_projects: list[Project] = []

    for i, proj in enumerate(resume.projects):
        with st.container():
            st.markdown(f"<p style='font-size:0.8rem; font-weight:600; color:var(--accent-color,#6366f1);'>Project {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Project Title", value=proj.title, key=f"proj_title_{i}", placeholder="AI Resume Builder")
                technologies = st.text_input("Technologies", value=proj.technologies, key=f"proj_tech_{i}", placeholder="Python, Streamlit, OpenAI")
            with col2:
                link = st.text_input("Project Link", value=proj.link, key=f"proj_link_{i}", placeholder="https://github.com/user/project")

            description = st.text_area(
                "Description",
                value=proj.description,
                key=f"proj_desc_{i}",
                height=100,
                placeholder="• Built an AI-powered resume builder that generates ATS-optimized resumes\n• Integrated GPT-4 for intelligent content enhancement",
            )

            updated_projects.append(Project(
                title=title, technologies=technologies,
                description=description, link=link,
            ))

            if i < len(resume.projects) - 1:
                st.markdown("<hr style='border-color:var(--border-color,rgba(255,255,255,0.06)); margin:0.5rem 0;'>", unsafe_allow_html=True)

    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Project", key="add_proj", use_container_width=True):
            updated_projects.append(Project())
    with col_remove:
        if len(updated_projects) > 1 and st.button("🗑️ Remove Last", key="rm_proj", use_container_width=True):
            updated_projects.pop()

    resume.projects = updated_projects
    _save_resume(resume)


def render_certifications_section() -> None:
    """Render certifications form section."""
    render_section_header("🏆", "Certifications", "Professional certifications and awards")

    resume = _get_resume()

    if not resume.certifications:
        resume.certifications = [Certification()]
        _save_resume(resume)

    updated_certs: list[Certification] = []

    for i, cert in enumerate(resume.certifications):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            title = st.text_input("Certification", value=cert.title, key=f"cert_title_{i}", placeholder="AWS Solutions Architect")
        with col2:
            issuer = st.text_input("Issuer", value=cert.issuer, key=f"cert_issuer_{i}", placeholder="Amazon Web Services")
        with col3:
            year = st.text_input("Year", value=cert.year, key=f"cert_year_{i}", placeholder="2024")

        updated_certs.append(Certification(title=title, issuer=issuer, year=year))

    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Certification", key="add_cert", use_container_width=True):
            updated_certs.append(Certification())
    with col_remove:
        if len(updated_certs) > 1 and st.button("🗑️ Remove Last", key="rm_cert", use_container_width=True):
            updated_certs.pop()

    resume.certifications = updated_certs
    _save_resume(resume)
