"""
Main dashboard — orchestrates all application tabs.

Each tab is rendered by a dedicated function that composes
UI components and service calls.
"""

from __future__ import annotations

import streamlit as st

from app.models.resume_schema import ResumeData
from app.utils.constants import (
    SESSION_RESUME_DATA,
    SESSION_ATS_RESULT,
    SESSION_JOB_DESCRIPTION,
    SESSION_SELECTED_TEMPLATE,
)
from app.utils.helpers import (
    get_session,
    set_session,
    init_session_state,
    validate_pdf_upload,
    queue_toast,
)
from app.ui.components import (
    render_section_header,
    render_score_ring,
    render_metric_bar,
    render_tag_list,
    render_glass_card,
    render_enhancement_diff,
    render_loading_skeleton,
)
from app.ui.form_sections import (
    render_personal_info_section,
    render_education_section,
    render_experience_section,
    render_skills_section,
    render_projects_section,
    render_certifications_section,
)
from app.config import AVAILABLE_TEMPLATES


# ===================================================================
# TAB 1: Resume Builder
# ===================================================================

def render_builder_tab() -> None:
    """Main resume builder form."""
    render_section_header("📝", "Resume Builder", "Fill in your details to build a professional resume")

    render_personal_info_section()
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    render_education_section()
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    render_experience_section()
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    render_skills_section()
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    render_projects_section()
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    render_certifications_section()


# ===================================================================
# TAB 2: Upload & Parse
# ===================================================================

def render_upload_tab() -> None:
    """PDF upload and AI parsing tab."""
    render_section_header("📄", "Upload & Parse Resume", "Upload a PDF resume and let AI extract all the details")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        key="pdf_uploader",
        help="Maximum file size: 5 MB",
    )

    if uploaded_file is not None:
        is_valid, error = validate_pdf_upload(uploaded_file)
        if not is_valid:
            st.error(f"❌ {error}")
            return

        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

        if st.button("🧠 Parse with AI", key="btn_parse", type="primary", use_container_width=True):
            with st.spinner("🔍 Extracting and analyzing resume content..."):
                render_loading_skeleton(5)
                try:
                    from app.services.parser_service import parse_uploaded_pdf

                    file_bytes = uploaded_file.getvalue()
                    resume_data = parse_uploaded_pdf(file_bytes)

                    set_session(SESSION_RESUME_DATA, resume_data)
                    queue_toast("Resume parsed successfully!", "✅")
                    st.rerun()

                except ValueError as e:
                    st.error(f"❌ Parsing failed: {str(e)}")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

    # Show parsed data preview
    resume = get_session(SESSION_RESUME_DATA)
    if resume and isinstance(resume, ResumeData) and not resume.is_empty():
        st.markdown("---")
        render_section_header("📋", "Parsed Data Preview")
        _render_resume_preview(resume)


def _render_resume_preview(resume: ResumeData) -> None:
    """Render a preview of parsed resume data."""
    pi = resume.personal_info

    if pi.name:
        st.markdown(f"**Name:** {pi.name}")
    if pi.email:
        st.markdown(f"**Email:** {pi.email}")
    if pi.phone:
        st.markdown(f"**Phone:** {pi.phone}")
    if pi.summary:
        st.markdown(f"**Summary:** {pi.summary[:200]}...")

    if resume.education:
        st.markdown(f"**Education:** {len(resume.education)} entries")
    if resume.experience:
        st.markdown(f"**Experience:** {len(resume.experience)} entries")
    if resume.skills:
        render_tag_list(resume.skills[:15], color="#6366f1", label="Skills")
    if resume.projects:
        st.markdown(f"**Projects:** {len(resume.projects)} entries")


# ===================================================================
# TAB 3: ATS Analysis
# ===================================================================

def render_ats_tab() -> None:
    """ATS analysis and job description matching tab."""
    render_section_header("🎯", "ATS Analysis", "Compare your resume against a job description")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("📝 Please build or upload your resume first.")
        return

    init_session_state(SESSION_JOB_DESCRIPTION, "")

    jd = st.text_area(
        "Paste the Job Description",
        value=get_session(SESSION_JOB_DESCRIPTION, ""),
        key="inp_jd",
        height=200,
        placeholder="Paste the full job description here for ATS analysis...",
    )
    set_session(SESSION_JOB_DESCRIPTION, jd)

    if st.button("🔍 Analyze ATS Match", key="btn_ats", type="primary", use_container_width=True):
        if not jd or len(jd.strip()) < 50:
            st.warning("⚠️ Please paste a detailed job description (at least 50 characters)")
            return

        with st.spinner("🧠 Analyzing ATS compatibility..."):
            try:
                from app.services.ats_service import analyze_ats_match

                result = analyze_ats_match(resume, jd)
                set_session(SESSION_ATS_RESULT, result)
                queue_toast("ATS analysis complete!", "🎯")
                st.rerun()

            except Exception as e:
                st.error(f"❌ ATS analysis failed: {str(e)}")

    # Display results
    ats = get_session(SESSION_ATS_RESULT)
    if ats:
        st.markdown("---")
        _render_ats_results(ats)


def _render_ats_results(ats) -> None:
    """Render ATS analysis results with visual indicators."""
    # Score rings
    cols = st.columns(4)
    with cols[0]:
        render_score_ring(ats.overall_score, "Overall")
    with cols[1]:
        render_score_ring(ats.keyword_score, "Keywords")
    with cols[2]:
        render_score_ring(ats.skills_match, "Skills")
    with cols[3]:
        render_score_ring(ats.experience_relevance, "Relevance")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Detail bars
    render_metric_bar("Keyword Coverage", ats.keyword_score)
    render_metric_bar("Experience Relevance", ats.experience_relevance)
    render_metric_bar("Skills Match", ats.skills_match)
    render_metric_bar("Formatting Score", ats.formatting_score)

    # Summary
    if ats.summary:
        render_glass_card(f"<p style='font-size:0.9rem; color:var(--text-primary,#e2e8f0);'>{ats.summary}</p>")

    # Keywords
    col1, col2 = st.columns(2)
    with col1:
        render_tag_list(ats.matched_keywords, color="#10b981", label="✅ Matched Keywords")
    with col2:
        render_tag_list(ats.missing_keywords, color="#ef4444", label="❌ Missing Keywords")

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        render_tag_list(ats.missing_skills, color="#f59e0b", label="⚠️ Missing Skills")
    with col4:
        render_tag_list(ats.missing_soft_skills, color="#8b5cf6", label="💡 Missing Soft Skills")

    # Suggestions
    if ats.suggestions:
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        render_section_header("💡", "Optimization Suggestions")
        for i, suggestion in enumerate(ats.suggestions):
            st.markdown(f"""
            <div style="
                padding:0.75rem 1rem; margin-bottom:0.5rem;
                background:rgba(99,102,241,0.06);
                border-left:3px solid #6366f1;
                border-radius:0 8px 8px 0;
            ">
                <span style="font-size:0.85rem; color:var(--text-primary,#e2e8f0);">{suggestion}</span>
            </div>
            """, unsafe_allow_html=True)


# ===================================================================
# TAB 4: AI Enhance
# ===================================================================

def render_enhance_tab() -> None:
    """AI-powered content enhancement tab."""
    render_section_header("✨", "AI Enhancement", "Supercharge your resume with AI-powered rewriting")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("📝 Please build or upload your resume first.")
        return

    # Summary Enhancement
    if resume.personal_info.summary:
        st.markdown("### 📝 Professional Summary")
        st.markdown(f"<div style='padding:0.75rem; background:rgba(255,255,255,0.03); border-radius:8px; font-size:0.85rem; color:var(--text-secondary,#94a3b8);'>{resume.personal_info.summary}</div>", unsafe_allow_html=True)
        if st.button("✨ Enhance Summary", key="enhance_summary"):
            with st.spinner("🧠 Rewriting summary..."):
                try:
                    from app.services.enhance_service import enhance_summary
                    result = enhance_summary(
                        resume.personal_info.summary,
                        skills=resume.skills,
                    )
                    render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                    if st.button("✅ Apply Enhancement", key="apply_summary"):
                        resume.personal_info.summary = result.enhanced
                        set_session(SESSION_RESUME_DATA, resume)
                        queue_toast("Summary updated!", "✅")
                        st.rerun()
                except Exception as e:
                    st.error(f"Enhancement failed: {str(e)}")

    st.markdown("---")

    # Experience Enhancement
    if resume.experience:
        st.markdown("### 💼 Work Experience")
        for i, exp in enumerate(resume.experience):
            if not exp.description:
                continue
            with st.expander(f"{exp.job_title or 'Position'} at {exp.company or 'Company'}", expanded=False):
                st.markdown(f"<p style='font-size:0.85rem; color:var(--text-secondary,#94a3b8);'>{exp.description[:300]}</p>", unsafe_allow_html=True)
                if st.button(f"✨ Enhance", key=f"enhance_exp_{i}"):
                    with st.spinner("🧠 Applying XYZ formula..."):
                        try:
                            from app.services.enhance_service import enhance_experience
                            result = enhance_experience(
                                exp.description,
                                job_title=exp.job_title,
                                company=exp.company,
                            )
                            render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                            if st.button("✅ Apply", key=f"apply_exp_{i}"):
                                resume.experience[i].description = result.enhanced
                                set_session(SESSION_RESUME_DATA, resume)
                                queue_toast("Experience updated!", "✅")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Enhancement failed: {str(e)}")

    st.markdown("---")

    # Project Enhancement
    if resume.projects:
        st.markdown("### 🚀 Projects")
        for i, proj in enumerate(resume.projects):
            if not proj.description:
                continue
            with st.expander(proj.title or f"Project {i + 1}", expanded=False):
                st.markdown(f"<p style='font-size:0.85rem; color:var(--text-secondary,#94a3b8);'>{proj.description[:300]}</p>", unsafe_allow_html=True)
                if st.button(f"✨ Enhance", key=f"enhance_proj_{i}"):
                    with st.spinner("🧠 Enhancing project description..."):
                        try:
                            from app.services.enhance_service import enhance_project
                            result = enhance_project(
                                proj.description,
                                project_title=proj.title,
                                technologies=proj.technologies,
                            )
                            render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                            if st.button("✅ Apply", key=f"apply_proj_{i}"):
                                resume.projects[i].description = result.enhanced
                                set_session(SESSION_RESUME_DATA, resume)
                                queue_toast("Project updated!", "✅")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Enhancement failed: {str(e)}")


# ===================================================================
# TAB 5: Export PDF
# ===================================================================

def render_export_tab() -> None:
    """PDF export tab with template selection."""
    render_section_header("📥", "Export Resume", "Choose a template and download your professional resume")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("📝 Please build or upload your resume first.")
        return

    init_session_state(SESSION_SELECTED_TEMPLATE, "tech_minimalist")

    # Template selection
    st.markdown("### 🎨 Choose Template")

    template_cols = st.columns(len(AVAILABLE_TEMPLATES))
    for idx, (key, name) in enumerate(AVAILABLE_TEMPLATES.items()):
        with template_cols[idx]:
            is_selected = get_session(SESSION_SELECTED_TEMPLATE) == key
            border_color = "#6366f1" if is_selected else "rgba(255,255,255,0.08)"
            bg = "rgba(99,102,241,0.1)" if is_selected else "rgba(255,255,255,0.02)"

            template_icons = {
                "tech_minimalist": "💻",
                "corporate_executive": "🏢",
                "modern_developer": "🚀",
            }
            icon = template_icons.get(key, "📄")

            st.markdown(f"""
            <div style="
                padding:1.2rem; text-align:center;
                border-radius:12px; border:2px solid {border_color};
                background:{bg}; cursor:pointer;
                transition: all 0.3s ease;
            ">
                <span style="font-size:2rem;">{icon}</span>
                <p style="font-size:0.85rem; font-weight:600; color:var(--text-primary,#e2e8f0); margin:0.5rem 0 0 0;">{name}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select", key=f"tmpl_{key}", use_container_width=True):
                set_session(SESSION_SELECTED_TEMPLATE, key)
                st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Generate button
    if st.button("📥 Generate & Download PDF", key="btn_generate", type="primary", use_container_width=True):
        with st.spinner("📄 Generating your professional resume..."):
            try:
                from app.services.pdf_service import generate_resume_pdf
                from app.database.db import save_resume, init_db

                template = get_session(SESSION_SELECTED_TEMPLATE, "tech_minimalist")

                filepath, filename = generate_resume_pdf(resume, template)

                # Save to database
                init_db()
                save_resume(resume, template)

                # Provide download
                with open(filepath, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label="⬇️ Download Resume PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success("✅ Resume generated successfully!")

            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
