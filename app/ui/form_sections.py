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
from app.ui.components import render_section_header, render_tag_list


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
        name = st.text_input("Full Name", value=pi.name, key="inp_name", placeholder="e.g. Jane Doe")
        email = st.text_input("Email Address", value=pi.email, key="inp_email", placeholder="e.g. jane@example.com")
        phone = st.text_input("Phone Number", value=pi.phone, key="inp_phone", placeholder="e.g. +1 (555) 123-4567")
    with col2:
        location = st.text_input("Location", value=pi.location, key="inp_location", placeholder="e.g. San Francisco, CA")
        linkedin = st.text_input("LinkedIn Profile URL", value=pi.linkedin, key="inp_linkedin", placeholder="e.g. https://linkedin.com/in/janedoe")
        github = st.text_input("GitHub Profile URL", value=pi.github, key="inp_github", placeholder="e.g. https://github.com/janedoe")

    summary = st.text_area(
        "Professional Summary",
        value=pi.summary,
        key="inp_summary",
        height=120,
        placeholder="A brief overview of your professional background, key achievements, and career goals...",
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
    render_section_header("🎓", "Education", "Your academic background and qualifications")

    resume = _get_resume()

    # Ensure at least one entry
    if not resume.education:
        resume.education = [Education()]
        _save_resume(resume)

    updated_education: list[Education] = []

    for i, edu in enumerate(resume.education):
        with st.container():
            st.markdown(f"<p style='font-size:0.75rem; font-weight:700; color:var(--accent-color); text-transform:uppercase; letter-spacing:0.05em;'>Education Entry {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                degree = st.text_input("Degree / Qualification", value=edu.degree, key=f"edu_degree_{i}", placeholder="e.g. B.S. in Computer Science")
                institution = st.text_input("Institution", value=edu.institution, key=f"edu_inst_{i}", placeholder="e.g. Stanford University")
            with col2:
                year = st.text_input("Duration / Graduation Year", value=edu.year, key=f"edu_year_{i}", placeholder="e.g. 2020 - 2024")
                gpa = st.text_input("GPA / Grade", value=edu.gpa, key=f"edu_gpa_{i}", placeholder="e.g. 3.8 / 4.0")
            
            highlights = st.text_input("Key Highlights / Honors (Optional)", value=edu.highlights, key=f"edu_hl_{i}", placeholder="e.g. Dean's List, Cum Laude, Relevant Coursework...")

            updated_education.append(Education(
                degree=degree, institution=institution,
                year=year, gpa=gpa, highlights=highlights,
            ))

            if i < len(resume.education) - 1:
                st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
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
    render_section_header("💼", "Work Experience", "Your professional history and achievements")

    resume = _get_resume()

    if not resume.experience:
        resume.experience = [WorkExperience()]
        _save_resume(resume)

    updated_experience: list[WorkExperience] = []

    for i, exp in enumerate(resume.experience):
        with st.container():
            st.markdown(f"<p style='font-size:0.75rem; font-weight:700; color:var(--accent-color); text-transform:uppercase; letter-spacing:0.05em;'>Position {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Job Title", value=exp.job_title, key=f"exp_title_{i}", placeholder="e.g. Senior Software Engineer")
                company = st.text_input("Company", value=exp.company, key=f"exp_company_{i}", placeholder="e.g. Acme Corp")
            with col2:
                duration = st.text_input("Duration", value=exp.duration, key=f"exp_dur_{i}", placeholder="e.g. Jan 2021 - Present")
                location = st.text_input("Location", value=exp.location, key=f"exp_loc_{i}", placeholder="e.g. New York, NY (Remote)")

            description = st.text_area(
                "Key Responsibilities & Achievements",
                value=exp.description,
                key=f"exp_desc_{i}",
                height=150,
                placeholder="• Architected a scalable microservices backend that improved API response times by 40%...\n• Mentored a team of 4 junior developers...",
            )

            updated_experience.append(WorkExperience(
                job_title=job_title, company=company,
                duration=duration, description=description,
                location=location,
            ))

            if i < len(resume.experience) - 1:
                st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Position", key="add_exp", use_container_width=True):
            updated_experience.append(WorkExperience())
    with col_remove:
        if len(updated_experience) > 1 and st.button("🗑️ Remove Last", key="rm_exp", use_container_width=True):
            updated_experience.pop()

    resume.experience = updated_experience
    _save_resume(resume)


def _add_suggested_skill(skill: str) -> None:
    """Callback to add a suggested skill and update session state before rendering."""
    resume = _get_resume()
    if skill not in resume.skills:
        resume.skills.append(skill)
        _save_resume(resume)
        st.session_state["inp_skills"] = skills_to_string(resume.skills)
    if "suggested_skills" in st.session_state and skill in st.session_state["suggested_skills"]:
        st.session_state["suggested_skills"].remove(skill)


def render_skills_section() -> None:
    """Render skills input section with AI suggestions."""
    render_section_header("🛠️", "Skills", "Your technical, domain, and soft skills")

    resume = _get_resume()
    current_skills = skills_to_string(resume.skills)

    skills_input = st.text_area(
        "List your skills (comma-separated)",
        value=current_skills,
        key="inp_skills",
        height=100,
        placeholder="e.g. Python, React, System Architecture, Agile Methodologies, AWS, Docker...",
    )

    resume.skills = skills_to_list(skills_input)
    _save_resume(resume)

    # 💡 AI Skill Suggester UI
    if "suggested_skills" not in st.session_state:
        st.session_state["suggested_skills"] = []

    col_btn, col_info = st.columns([1.5, 2.5])
    with col_btn:
        if st.button("✨ Auto-Suggest Skills", key="btn_suggest_skills", use_container_width=True):
            exp_context = ""
            for idx, exp in enumerate(resume.experience):
                if exp.job_title:
                    exp_context += f"Job Title: {exp.job_title}\n"
                if exp.company:
                    exp_context += f"Company: {exp.company}\n"
                if exp.description:
                    exp_context += f"Description:\n{exp.description}\n"
                exp_context += "---\n"

            if not exp_context.strip():
                st.warning("⚠️ Add work experience first to get relevant suggestions!")
            else:
                with st.spinner("🧠 Recommending skills..."):
                    try:
                        from app.services.ai_service import ai_service
                        prompt = f"""You are an expert resume assistant. Analyze the candidate's work experiences and suggest 8 highly relevant technical or soft skills they should add to their resume.

Candidate Experiences:
{exp_context}

Return ONLY valid JSON with this exact structure:
{{
    "skills": ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5", "Skill 6", "Skill 7", "Skill 8"]
}}"""
                        res = ai_service.generate_json(
                            system_prompt="You are a professional resume writer and recruitment specialist.",
                            user_prompt=prompt,
                        )
                        st.session_state["suggested_skills"] = res.get("skills", [])
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Skill suggestion failed: {str(e)}")

    if st.session_state["suggested_skills"]:
        st.markdown("<p style='font-size:0.825rem; font-weight:600; color:var(--text-secondary); margin: 0.5rem 0 0.25rem 0;'>💡 Suggested Skills (Click to add):</p>", unsafe_allow_html=True)
        suggested = st.session_state["suggested_skills"]
        
        # Render chips inside small columns
        cols = st.columns(4)
        for idx, skill in enumerate(suggested):
            col_idx = idx % 4
            with cols[col_idx]:
                st.button(
                    f"➕ {skill}",
                    key=f"add_suggested_skill_{idx}",
                    use_container_width=True,
                    type="secondary",
                    on_click=_add_suggested_skill,
                    args=(skill,),
                )

    # Preview tags
    if resume.skills:
        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
        render_tag_list(resume.skills, color="var(--accent-color)", label="Skills Preview")


def render_projects_section() -> None:
    """Render projects form section with dynamic entries."""
    render_section_header("🚀", "Projects", "Showcase your best work and personal projects")

    resume = _get_resume()

    if not resume.projects:
        resume.projects = [Project()]
        _save_resume(resume)

    updated_projects: list[Project] = []

    for i, proj in enumerate(resume.projects):
        with st.container():
            st.markdown(f"<p style='font-size:0.75rem; font-weight:700; color:var(--accent-color); text-transform:uppercase; letter-spacing:0.05em;'>Project {i + 1}</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Project Name", value=proj.title, key=f"proj_title_{i}", placeholder="e.g. E-Commerce Platform")
                technologies = st.text_input("Technologies Used", value=proj.technologies, key=f"proj_tech_{i}", placeholder="e.g. Next.js, Stripe, PostgreSQL")
            with col2:
                link = st.text_input("Project URL (GitHub / Live)", value=proj.link, key=f"proj_link_{i}", placeholder="e.g. https://github.com/user/repo")

            description = st.text_area(
                "Project Description",
                value=proj.description,
                key=f"proj_desc_{i}",
                height=120,
                placeholder="• Developed a high-performance e-commerce platform processing $10k+ in monthly transactions...\n• Integrated automated testing pipeline reducing bugs by 30%...",
            )

            updated_projects.append(Project(
                title=title, technologies=technologies,
                description=description, link=link,
            ))

            if i < len(resume.projects) - 1:
                st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
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
    render_section_header("🏆", "Certifications", "Professional certifications, licenses, and awards")

    resume = _get_resume()

    if not resume.certifications:
        resume.certifications = [Certification()]
        _save_resume(resume)

    updated_certs: list[Certification] = []

    for i, cert in enumerate(resume.certifications):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            title = st.text_input("Certification Name", value=cert.title, key=f"cert_title_{i}", placeholder="e.g. AWS Certified Solutions Architect")
        with col2:
            issuer = st.text_input("Issuing Organization", value=cert.issuer, key=f"cert_issuer_{i}", placeholder="e.g. Amazon Web Services")
        with col3:
            year = st.text_input("Year", value=cert.year, key=f"cert_year_{i}", placeholder="e.g. 2024")

        updated_certs.append(Certification(title=title, issuer=issuer, year=year))

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    col_add, col_remove = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add Certification", key="add_cert", use_container_width=True):
            updated_certs.append(Certification())
    with col_remove:
        if len(updated_certs) > 1 and st.button("🗑️ Remove Last", key="rm_cert", use_container_width=True):
            updated_certs.pop()

    resume.certifications = updated_certs
    _save_resume(resume)
