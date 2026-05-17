"""
Main dashboard — orchestrates all application tabs.

Each tab is rendered by a dedicated function that composes
premium UI components and service calls.
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
    render_section_header("📝", "Resume Builder", "Build your professional profile block by block.")

    render_personal_info_section()
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    render_education_section()
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    render_experience_section()
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    render_skills_section()
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    render_projects_section()
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    render_certifications_section()


# ===================================================================
# TAB 2: Upload & Parse
# ===================================================================

def render_upload_tab() -> None:
    """PDF upload and AI parsing tab."""
    render_section_header("📄", "Upload & Parse", "Let AI extract all details directly from your existing PDF resume.")

    uploaded_file = st.file_uploader(
        "Drop your PDF resume here",
        type=["pdf"],
        key="pdf_uploader",
        help="Maximum file size: 5 MB",
    )

    if uploaded_file is not None:
        is_valid, error = validate_pdf_upload(uploaded_file)
        if not is_valid:
            st.error(f"❌ {error}")
            return

        st.success(f"✅ File uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

        if st.button("🧠 Parse with AI", key="btn_parse", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing document structure and extracting data..."):
                render_loading_skeleton(4)
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
        st.markdown("<hr style='margin:3rem 0;'>", unsafe_allow_html=True)
        render_section_header("📋", "Parsed Data Preview", "Verify the extracted information before proceeding.")
        _render_resume_preview(resume)


def _render_resume_preview(resume: ResumeData) -> None:
    """Render a preview of parsed resume data in a glass card."""
    pi = resume.personal_info
    
    html = "<div style='line-height: 1.8;'>"
    if pi.name:
        html += f"<p><strong>Name:</strong> <span style='color:var(--text-secondary);'>{pi.name}</span></p>"
    if pi.email:
        html += f"<p><strong>Email:</strong> <span style='color:var(--text-secondary);'>{pi.email}</span></p>"
    if pi.phone:
        html += f"<p><strong>Phone:</strong> <span style='color:var(--text-secondary);'>{pi.phone}</span></p>"
    if pi.summary:
        html += f"<p><strong>Summary:</strong> <span style='color:var(--text-secondary);'>{pi.summary[:150]}...</span></p>"
        
    html += "<div style='display:flex; gap:1.5rem; margin-top:1.5rem; padding-top:1.5rem; border-top:1px solid var(--border-color);'>"
    if resume.education:
        html += f"<div><strong>🎓 Education:</strong> <span style='color:var(--text-secondary);'>{len(resume.education)} entries</span></div>"
    if resume.experience:
        html += f"<div><strong>💼 Experience:</strong> <span style='color:var(--text-secondary);'>{len(resume.experience)} entries</span></div>"
    if resume.projects:
        html += f"<div><strong>🚀 Projects:</strong> <span style='color:var(--text-secondary);'>{len(resume.projects)} entries</span></div>"
    html += "</div></div>"
    
    render_glass_card(html)
    
    if resume.skills:
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        render_tag_list(resume.skills[:15], color="var(--accent-color)", label="Extracted Skills")


# ===================================================================
# TAB 3: ATS Analysis
# ===================================================================

def render_ats_tab() -> None:
    """ATS analysis and job description matching tab."""
    render_section_header("🎯", "ATS Analysis", "Compare your resume against a target job description to uncover missing keywords.")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("💡 **Tip:** Please build or upload your resume in the previous tabs first.")
        return

    init_session_state(SESSION_JOB_DESCRIPTION, "")

    jd = st.text_area(
        "Target Job Description",
        value=get_session(SESSION_JOB_DESCRIPTION, ""),
        key="inp_jd",
        height=200,
        placeholder="Paste the full job description here (responsibilities, requirements, preferred qualifications)...",
    )
    set_session(SESSION_JOB_DESCRIPTION, jd)

    if st.button("🔍 Run Deep Analysis", key="btn_ats", type="primary", use_container_width=True):
        if not jd or len(jd.strip()) < 50:
            st.warning("⚠️ Please paste a detailed job description (minimum 50 characters).")
            return

        with st.spinner("🧠 Scanning for keywords, skills, and relevance..."):
            try:
                from app.services.ats_service import analyze_ats_match

                result = analyze_ats_match(resume, jd)
                set_session(SESSION_ATS_RESULT, result)
                queue_toast("ATS Analysis Complete!", "🎯")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

    # Display results
    ats = get_session(SESSION_ATS_RESULT)
    if ats:
        st.markdown("<hr style='margin:3rem 0;'>", unsafe_allow_html=True)
        _render_ats_results(ats)


def _render_ats_results(ats) -> None:
    """Render ATS analysis results with visual indicators."""
    st.markdown("<h3 style='margin-bottom:1.5rem;'>Analysis Results</h3>", unsafe_allow_html=True)
    
    # Score rings
    cols = st.columns(4)
    with cols[0]:
        render_score_ring(ats.overall_score, "Overall Match")
    with cols[1]:
        render_score_ring(ats.keyword_score, "Keywords")
    with cols[2]:
        render_score_ring(ats.skills_match, "Core Skills")
    with cols[3]:
        render_score_ring(ats.experience_relevance, "Relevance")

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    # Detail bars
    render_metric_bar("Keyword Coverage", ats.keyword_score)
    render_metric_bar("Experience Relevance", ats.experience_relevance)
    render_metric_bar("Skills Alignment", ats.skills_match)
    render_metric_bar("Formatting Score", ats.formatting_score)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Summary
    if ats.summary:
        render_glass_card(f"<p style='font-size:0.95rem; line-height:1.6; color:var(--text-primary); margin:0;'>{ats.summary}</p>")

    # Keywords
    col1, col2 = st.columns(2)
    with col1:
        render_tag_list(ats.matched_keywords, color="#10b981", label="✅ Matched Keywords")
    with col2:
        render_tag_list(ats.missing_keywords, color="#ef4444", label="❌ Missing Keywords")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        render_tag_list(ats.missing_skills, color="#f59e0b", label="⚠️ Missing Hard Skills")
    with col4:
        render_tag_list(ats.missing_soft_skills, color="#8b5cf6", label="💡 Missing Soft Skills")

    # Suggestions
    if ats.suggestions:
        st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:1rem; color:var(--text-primary);'>Actionable Next Steps</h4>", unsafe_allow_html=True)
        for i, suggestion in enumerate(ats.suggestions):
            st.markdown(f"""
            <div style="
                padding:1rem 1.25rem; margin-bottom:0.75rem;
                background:var(--input-bg);
                border-left:4px solid var(--accent-color);
                border-radius:0 8px 8px 0;
                box-shadow: 0 2px 8px var(--shadow-color);
            ">
                <span style="font-size:0.9rem; font-weight:500; color:var(--text-primary);">{suggestion}</span>
            </div>
            """, unsafe_allow_html=True)


# ===================================================================
# TAB 4: AI Enhance
# ===================================================================

def render_enhance_tab() -> None:
    """AI-powered content enhancement tab."""
    render_section_header("✨", "AI Enhancement", "Supercharge your bullet points using the Google XYZ formula and AI rewriting.")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("💡 **Tip:** Please build or upload your resume in the previous tabs first.")
        return

    # Summary Enhancement
    if resume.personal_info.summary:
        st.markdown("### 📝 Professional Summary")
        render_glass_card(f"<div style='font-size:0.9rem; color:var(--text-secondary);'>{resume.personal_info.summary}</div>", padding="1.5rem")
        if st.button("✨ Auto-Enhance Summary", key="enhance_summary"):
            with st.spinner("🧠 Rewriting summary..."):
                try:
                    from app.services.enhance_service import enhance_summary
                    result = enhance_summary(
                        resume.personal_info.summary,
                        skills=resume.skills,
                    )
                    render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                    if st.button("✅ Apply Enhancement to Profile", key="apply_summary", type="primary"):
                        resume.personal_info.summary = result.enhanced
                        set_session(SESSION_RESUME_DATA, resume)
                        queue_toast("Summary updated successfully!", "✅")
                        st.rerun()
                except Exception as e:
                    st.error(f"Enhancement failed: {str(e)}")

    st.markdown("<hr style='margin:3rem 0;'>", unsafe_allow_html=True)

    # Experience Enhancement
    if resume.experience:
        st.markdown("### 💼 Work Experience")
        for i, exp in enumerate(resume.experience):
            if not exp.description:
                continue
            with st.expander(f"{exp.job_title or 'Position'} at {exp.company or 'Company'}", expanded=False):
                st.markdown(f"<p style='font-size:0.9rem; color:var(--text-secondary); white-space:pre-wrap;'>{exp.description}</p>", unsafe_allow_html=True)
                if st.button(f"✨ Apply XYZ Formula", key=f"enhance_exp_{i}"):
                    with st.spinner("🧠 Rewriting bullets using impact metrics..."):
                        try:
                            from app.services.enhance_service import enhance_experience
                            result = enhance_experience(
                                exp.description,
                                job_title=exp.job_title,
                                company=exp.company,
                            )
                            render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                            if st.button("✅ Apply to Profile", key=f"apply_exp_{i}", type="primary"):
                                resume.experience[i].description = result.enhanced
                                set_session(SESSION_RESUME_DATA, resume)
                                queue_toast("Experience updated!", "✅")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Enhancement failed: {str(e)}")

    st.markdown("<hr style='margin:3rem 0;'>", unsafe_allow_html=True)

    # Project Enhancement
    if resume.projects:
        st.markdown("### 🚀 Projects")
        for i, proj in enumerate(resume.projects):
            if not proj.description:
                continue
            with st.expander(proj.title or f"Project {i + 1}", expanded=False):
                st.markdown(f"<p style='font-size:0.9rem; color:var(--text-secondary); white-space:pre-wrap;'>{proj.description}</p>", unsafe_allow_html=True)
                if st.button(f"✨ Enhance Project Metrics", key=f"enhance_proj_{i}"):
                    with st.spinner("🧠 Optimizing project description..."):
                        try:
                            from app.services.enhance_service import enhance_project
                            result = enhance_project(
                                proj.description,
                                project_title=proj.title,
                                technologies=proj.technologies,
                            )
                            render_enhancement_diff(result.original, result.enhanced, result.changes_made)
                            if st.button("✅ Apply to Profile", key=f"apply_proj_{i}", type="primary"):
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
    render_section_header("📥", "Export Resume", "Choose a premium template and download your professional resume.")

    resume = get_session(SESSION_RESUME_DATA)
    if not resume or not isinstance(resume, ResumeData) or resume.is_empty():
        st.info("💡 **Tip:** Please build or upload your resume in the previous tabs first.")
        return

    init_session_state(SESSION_SELECTED_TEMPLATE, "tech_minimalist")

    # Template selection
    st.markdown("<h3 style='margin-bottom:1.5rem;'>🎨 Choose Template</h3>", unsafe_allow_html=True)

    template_cols = st.columns(len(AVAILABLE_TEMPLATES))
    for idx, (key, name) in enumerate(AVAILABLE_TEMPLATES.items()):
        with template_cols[idx]:
            is_selected = get_session(SESSION_SELECTED_TEMPLATE) == key
            border_color = "var(--accent-color)" if is_selected else "var(--border-color)"
            bg = "rgba(99,102,241,0.05)" if is_selected else "var(--card-bg)"
            shadow = "0 8px 24px rgba(99,102,241,0.2)" if is_selected else "0 4px 12px var(--shadow-color)"

            template_icons = {
                "tech_minimalist": "💻",
                "corporate_executive": "🏢",
                "modern_developer": "🚀",
            }
            icon = template_icons.get(key, "📄")

            st.markdown(f"""
            <div style="
                padding:2rem 1rem; text-align:center;
                border-radius:16px; border:2px solid {border_color};
                background:{bg}; cursor:pointer;
                box-shadow: {shadow};
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                margin-bottom:1rem;
            ">
                <span style="font-size:2.5rem; filter:drop-shadow(0 4px 6px rgba(0,0,0,0.1));">{icon}</span>
                <p style="font-size:0.95rem; font-weight:700; color:var(--text-primary); margin:1rem 0 0 0;">{name}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select Template", key=f"tmpl_{key}", use_container_width=True, type="primary" if is_selected else "secondary"):
                set_session(SESSION_SELECTED_TEMPLATE, key)
                st.rerun()

    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)

    # Generate button
    if st.button("📥 Generate & Download PDF", key="btn_generate", type="primary", use_container_width=True):
        with st.spinner("📄 Compiling professional PDF..."):
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
                    label="⬇️ Download Your Resume",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
                st.success("✅ PDF generated successfully! Ready for download.")

            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
