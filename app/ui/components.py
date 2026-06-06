"""
Reusable UI components for the application.

Contains styled cards, score displays, loading states,
toast handlers, and other visual building blocks tailored
for premium dark/light mode aesthetics.
"""

from __future__ import annotations

import streamlit as st

from app.utils.helpers import format_score_color, format_score_label


def render_score_ring(score: int, label: str, size: int = 120) -> None:
    """Render an animated circular score indicator."""
    color = format_score_color(score)
    grade = format_score_label(score)

    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; padding:1.5rem 1rem;">
        <div style="
            width:{size}px; height:{size}px;
            border-radius:50%;
            background: conic-gradient({color} {score * 3.6}deg, var(--border-color) {score * 3.6}deg);
            display:flex; align-items:center; justify-content:center;
            box-shadow: 0 0 24px {color}25, inset 0 4px 12px rgba(0,0,0,0.1);
            animation: scorePopIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        ">
            <div style="
                width:{size - 14}px; height:{size - 14}px;
                border-radius:50%;
                background: var(--bg-primary);
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                box-shadow: inset 0 2px 8px var(--shadow-color);
            ">
                <span style="font-size:2rem; font-weight:800; color:{color}; letter-spacing:-0.05em; line-height:1;">{score}</span>
                <span style="font-size:0.6rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.1em; margin-top:0.25rem;">{label}</span>
            </div>
        </div>
        <span style="margin-top:1rem; font-size:0.85rem; font-weight:600; color:{color};">{grade}</span>
    </div>
    """, unsafe_allow_html=True)


def render_metric_bar(label: str, value: int, max_value: int = 100) -> None:
    """Render a horizontal progress bar with label."""
    color = format_score_color(value)
    pct = min(value / max_value * 100, 100)

    st.markdown(f"""
    <div style="margin-bottom:1.25rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
            <span style="font-size:0.85rem; font-weight:500; color:var(--text-secondary);">{label}</span>
            <span style="font-size:0.85rem; font-weight:700; color:{color};">{value}%</span>
        </div>
        <div style="
            height:8px; border-radius:4px;
            background:var(--border-color);
            overflow:hidden;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
        ">
            <div style="
                height:100%; width:{pct}%;
                border-radius:4px;
                background: linear-gradient(90deg, {color}aa, {color});
                transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: 0 0 10px {color}55;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_tag_list(tags: list[str], color: str = "var(--accent-color)", label: str = "") -> None:
    """Render a list of tags/chips."""
    if not tags:
        return
    if label:
        st.markdown(f"<p style='font-size:0.75rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem;'>{label}</p>", unsafe_allow_html=True)

    tags_html = " ".join([
        f"<span style='display:inline-flex; align-items:center; padding:0.35rem 0.75rem; margin:0.2rem; "
        f"border-radius:9999px; font-size:0.8rem; font-weight:500; "
        f"background:var(--input-bg); color:{color}; border:1px solid var(--border-color); "
        f"box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition:all 0.2s ease;'>{t}</span>"
        for t in tags
    ])
    st.markdown(f"<div style='line-height:2.2; margin-bottom:1rem;'>{tags_html}</div>", unsafe_allow_html=True)


def render_glass_card(content_html: str, padding: str = "2rem") -> None:
    """Render a glassmorphism-styled card."""
    st.markdown(f"""
    <div style="
        background: var(--card-bg);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: {padding};
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px var(--shadow-color);
        transition: all 0.3s ease;
    ">
        {content_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(icon: str, title: str, subtitle: str = "") -> None:
    """Render a styled section header."""
    sub_html = f"<p style='font-size:0.9rem; color:var(--text-secondary); margin:0.25rem 0 0 0; line-height:1.5;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom:2rem; padding-bottom:1rem; border-bottom:1px solid var(--border-color);">
        <h2 style="
            display:flex; align-items:center; gap:0.5rem;
            font-size:1.75rem; font-weight:800; letter-spacing:-0.03em;
            color:var(--text-primary);
            margin:0;
        ">
            <span style="font-size:1.5rem; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.1));">{icon}</span> 
            {title}
        </h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_enhancement_diff(original: str, enhanced: str, changes: list[str]) -> None:
    """Show a before/after comparison for AI enhancements."""
    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin:1.5rem 0;">
        <div style="
            padding:1.25rem; border-radius:12px; 
            background:rgba(239,68,68,0.05); 
            border:1px solid rgba(239,68,68,0.2);
        ">
            <p style="
                font-size:0.75rem; font-weight:700; color:#ef4444; 
                margin-bottom:0.75rem; text-transform:uppercase; letter-spacing:0.05em;
                display:flex; align-items:center; gap:0.35rem;
            "><span>❌</span> Original</p>
            <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6; margin:0;">""" + original.replace('\n', '<br>') + """</p>
        </div>
        <div style="
            padding:1.25rem; border-radius:12px; 
            background:rgba(16,185,129,0.05); 
            border:1px solid rgba(16,185,129,0.2);
            box-shadow: 0 4px 20px rgba(16,185,129,0.08);
        ">
            <p style="
                font-size:0.75rem; font-weight:700; color:#10b981; 
                margin-bottom:0.75rem; text-transform:uppercase; letter-spacing:0.05em;
                display:flex; align-items:center; gap:0.35rem;
            "><span>✨</span> Enhanced</p>
            <p style="font-size:0.9rem; color:var(--text-primary); font-weight:500; line-height:1.6; margin:0;">""" + enhanced.replace('\n', '<br>') + """</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if changes:
        with st.expander("📝 View specific changes made"):
            st.markdown("<ul style='color:var(--text-secondary); font-size:0.9rem; line-height:1.6;'>", unsafe_allow_html=True)
            for change in changes:
                st.markdown(f"<li>{change}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)


def render_loading_skeleton(lines: int = 3) -> None:
    """Render a premium loading skeleton placeholder."""
    skeleton_lines = ""
    for i in range(lines):
        width = 100 - (i * 15)
        skeleton_lines += f"""
        <div style="
            height:14px; width:{width}%;
            background: linear-gradient(90deg, var(--input-bg) 25%, var(--border-color) 50%, var(--input-bg) 75%);
            background-size: 200% 100%;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            animation: shimmer 1.5s infinite linear;
        "></div>
        """
    st.markdown(f"""
    <div style="
        padding:1.5rem; border:1px solid var(--border-color); 
        border-radius:12px; background:var(--card-bg);
    ">
        {skeleton_lines}
    </div>
    """, unsafe_allow_html=True)


def render_completion_tracker(resume_data) -> None:
    """Render a section completion progress tracker."""
    sections = {
        "Personal Info": bool(resume_data.personal_info.name and resume_data.personal_info.email),
        "Summary": bool(resume_data.personal_info.summary),
        "Education": bool(resume_data.education),
        "Experience": bool(resume_data.experience),
        "Skills": bool(resume_data.skills),
        "Projects": bool(resume_data.projects),
    }

    completed = sum(sections.values())
    total = len(sections)
    pct = int(completed / total * 100)

    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem; align-items:flex-end;">
            <span style="font-size:0.7rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em;">Completion</span>
            <span style="font-size:0.9rem; font-weight:800; color:var(--accent-color);">{pct}%</span>
        </div>
        <div style="
            height:6px; border-radius:3px; 
            background:var(--input-bg);
            border: 1px solid var(--border-color);
            overflow:hidden;
        ">
            <div style="
                height:100%; width:{pct}%; 
                border-radius:3px; 
                background:linear-gradient(90deg, var(--accent-color), #8b5cf6); 
                transition:width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: 0 0 8px rgba(99,102,241,0.5);
            "></div>
        </div>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
    """, unsafe_allow_html=True)

    for name, done in sections.items():
        icon = "✅" if done else "○"
        color = "var(--text-primary)" if done else "var(--text-muted)"
        opacity = "1" if done else "0.5"
        st.markdown(f"""
        <div style="
            font-size:0.75rem; font-weight:500; color:{color}; 
            opacity:{opacity}; display:flex; align-items:center; gap:0.3rem;
        ">
            <span>{icon}</span> {name}
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)


def render_live_resume_preview(resume_data, template_key: str = "tech_minimalist") -> None:
    """Render a premium HTML/CSS-based live resume sheet with distinct layouts per template."""
    import textwrap
    from app.utils.constants import TEMPLATE_COLORS
    
    colors = TEMPLATE_COLORS.get(template_key, TEMPLATE_COLORS["tech_minimalist"])
    
    # Map colors
    p_color = f"rgb{colors['primary']}"
    s_color = f"rgb{colors['secondary']}"
    a_color = f"rgb{colors['accent']}"
    t_color = f"rgb{colors['text']}"
    l_color = f"rgb{colors['light']}"
    
    pi = resume_data.personal_info
    
    # Build sections depending on template type
    if template_key == "corporate_executive":
        font_family = "'Georgia', serif"
        section_title_style = f"color: {p_color}; font-size: 1.05rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; text-align: center; border-bottom: 2px double {p_color}; padding-bottom: 0.2rem; margin: 1.5rem 0 0.75rem 0;"
    elif template_key == "modern_developer":
        font_family = "'Outfit', sans-serif"
        section_title_style = f"color: {p_color}; font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; margin: 1.5rem 0 0.75rem 0; border-bottom: 2px solid {p_color}; padding-bottom: 0.25rem;"
    else: # tech_minimalist
        font_family = "'Inter', sans-serif"
        section_title_style = f"color: {p_color}; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border-left: 4px solid {p_color}; padding-left: 0.5rem; margin: 1.5rem 0 0.75rem 0;"

    # 1. Header Section
    if template_key == "corporate_executive":
        contacts = []
        if pi.email: contacts.append(pi.email)
        if pi.phone: contacts.append(pi.phone)
        if pi.location: contacts.append(pi.location)
        if pi.linkedin: contacts.append(f"<a href='{pi.linkedin}' target='_blank' style='color:{t_color}; text-decoration:none;'>LinkedIn</a>")
        if pi.github: contacts.append(f"<a href='{pi.github}' target='_blank' style='color:{t_color}; text-decoration:none;'>GitHub</a>")
        contact_str = "  •  ".join(contacts)
        
        header_html = f"""
        <div style="text-align: center; margin-bottom: 1.5rem; border-bottom: 1px solid {l_color}; padding-bottom: 1rem;">
            <h1 style="color: {t_color} !important; font-size: 2.2rem; font-weight: 700; margin: 0; font-family: {font_family};">{pi.name or "Your Name"}</h1>
            <div style="font-size: 0.8rem; color: {s_color}; margin-top: 0.5rem; font-family: {font_family};">
                {contact_str}
            </div>
        </div>
        """
    elif template_key == "modern_developer":
        links_list = []
        if pi.email: links_list.append(f"<span>✉️ {pi.email}</span>")
        if pi.phone: links_list.append(f"<span>📞 {pi.phone}</span>")
        if pi.location: links_list.append(f"<span>📍 {pi.location}</span>")
        if pi.linkedin: links_list.append(f"<span>🔗 <a href='{pi.linkedin}' target='_blank' style='color:{p_color}; text-decoration:none;'>LinkedIn</a></span>")
        if pi.github: links_list.append(f"<span>💻 <a href='{pi.github}' target='_blank' style='color:{p_color}; text-decoration:none;'>GitHub</a></span>")
        
        header_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid {p_color}; padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <div>
                <h1 style="color: #1e293b !important; font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -0.04em;">{pi.name or "Your Name"}</h1>
                <p style="color: {p_color}; margin: 0.25rem 0 0 0; font-weight: 600; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em;">Developer / Engineer</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem; font-size: 0.75rem; color: {s_color}; font-weight: 500;">
                {"".join(links_list)}
            </div>
        </div>
        """
    else:  # tech_minimalist
        links_list = []
        if pi.email: links_list.append(f"<span>{pi.email}</span>")
        if pi.phone: links_list.append(f"<span>{pi.phone}</span>")
        if pi.location: links_list.append(f"<span>{pi.location}</span>")
        if pi.linkedin: links_list.append(f"<a href='{pi.linkedin}' target='_blank' style='color:{p_color}; text-decoration:none;'>LinkedIn</a>")
        if pi.github: links_list.append(f"<a href='{pi.github}' target='_blank' style='color:{p_color}; text-decoration:none;'>GitHub</a>")
        
        header_html = f"""
        <div style="margin-bottom: 1.5rem; border-bottom: 1px solid {l_color}; padding-bottom: 1rem;">
            <h1 style="color: #1e293b !important; font-size: 1.8rem; font-weight: 800; margin: 0; letter-spacing: -0.03em;">{pi.name or "Your Name"}</h1>
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.75rem; color: {s_color}; margin-top: 0.4rem; font-weight: 500;">
                {"  |  ".join(links_list)}
            </div>
        </div>
        """

    # 2. Summary Section
    summary_html = ""
    if pi.summary:
        summary_html = f"""
        <div style="margin-bottom: 1.25rem;">
            <h3 style="{section_title_style}">Professional Summary</h3>
            <p style="color: #334155; font-size: 0.85rem; margin: 0; line-height: 1.5; font-family: {font_family}; text-align: justify;">{pi.summary}</p>
        </div>
        """

    # 3. Experience Section
    exp_html = ""
    if resume_data.experience:
        exp_entries = ""
        for exp in resume_data.experience:
            if not exp.job_title and not exp.company:
                continue
            desc_list = ""
            if exp.description:
                bullets = [b.strip() for b in exp.description.split("\n") if b.strip()]
                for bullet in bullets:
                    bullet_text = bullet.lstrip("•-* ")
                    if bullet_text:
                        desc_list += f"<li style='margin-bottom: 0.25rem;'>{bullet_text}</li>"
            
            exp_entries += f"""
            <div style="margin-bottom: 0.9rem; font-family: {font_family};">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.15rem;">
                    <strong style="color: #1e293b; font-size: 0.9rem;">{exp.job_title or "Job Title"}</strong>
                    <span style="font-size: 0.75rem; color: {s_color}; font-weight: 500;">{exp.duration or "Duration"}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; font-size: 0.8rem; color: {s_color}; font-weight: 500; margin-bottom: 0.35rem;">
                    <span style="font-style: italic;">{exp.company or "Company"} {f'— {exp.location}' if exp.location else ''}</span>
                </div>
                {"<ul style='color: #334155; font-size: 0.8rem; margin: 0; padding-left: 1.2rem; line-height: 1.45;'>" + desc_list + "</ul>" if desc_list else ""}
            </div>
            """
        if exp_entries:
            exp_html = f"""
            <div style="margin-bottom: 1.25rem;">
                <h3 style="{section_title_style}">Work Experience</h3>
                {exp_entries}
            </div>
            """

    # 4. Education Section
    edu_html = ""
    if resume_data.education:
        edu_entries = ""
        for edu in resume_data.education:
            if not edu.degree and not edu.institution:
                continue
            edu_entries += f"""
            <div style="margin-bottom: 0.75rem; font-family: {font_family};">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.15rem;">
                    <strong style="color: #1e293b; font-size: 0.9rem;">{edu.degree or "Degree"}</strong>
                    <span style="font-size: 0.75rem; color: {s_color}; font-weight: 500;">{edu.year or "Graduation Year"}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; font-size: 0.8rem; color: {s_color}; font-weight: 500;">
                    <span>{edu.institution or "Institution"} {f'• GPA: {edu.gpa}' if edu.gpa else ''}</span>
                </div>
                {f"<p style='color: {s_color}; font-size: 0.75rem; margin: 0.15rem 0 0 0; font-style: italic;'>{edu.highlights}</p>" if edu.highlights else ""}
            </div>
            """
        if edu_entries:
            edu_html = f"""
            <div style="margin-bottom: 1.25rem;">
                <h3 style="{section_title_style}">Education</h3>
                {edu_entries}
            </div>
            """

    # 5. Projects Section
    proj_html = ""
    if resume_data.projects:
        proj_entries = ""
        for proj in resume_data.projects:
            if not proj.title:
                continue
            desc_list = ""
            if proj.description:
                bullets = [b.strip() for b in proj.description.split("\n") if b.strip()]
                for bullet in bullets:
                    bullet_text = bullet.lstrip("•-* ")
                    if bullet_text:
                        desc_list += f"<li style='margin-bottom: 0.2rem;'>{bullet_text}</li>"
            
            proj_title_display = proj.title
            if proj.link:
                proj_title_display = f"<a href='{proj.link}' target='_blank' style='color:{p_color}; text-decoration:none;'>{proj.title} 🔗</a>"
                
            proj_entries += f"""
            <div style="margin-bottom: 0.75rem; font-family: {font_family};">
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.15rem;">
                    <strong style="color: #1e293b; font-size: 0.9rem;">{proj_title_display}</strong>
                    {f"<span style='font-size: 0.75rem; color: {s_color}; font-style: italic;'>{proj.technologies}</span>" if proj.technologies else ""}
                </div>
                {"<ul style='color: #334155; font-size: 0.8rem; margin: 0; padding-left: 1.2rem; line-height: 1.45;'>" + desc_list + "</ul>" if desc_list else ""}
            </div>
            """
        if proj_entries:
            proj_html = f"""
            <div style="margin-bottom: 1.25rem;">
                <h3 style="{section_title_style}">Projects</h3>
                {proj_entries}
            </div>
            """

    # 6. Skills Section
    skills_html = ""
    if resume_data.skills:
        if template_key == "modern_developer":
            # Render skills as tech pills in the preview
            skills_pills = "".join([
                f"<span style='display:inline-block; padding:0.2rem 0.5rem; margin:0.15rem; "
                f"border-radius:4px; font-size:0.75rem; font-family:monospace; "
                f"background:{l_color}; color:{p_color}; border:1px solid rgba(0,0,0,0.05);'>{s}</span>"
                for s in resume_data.skills
            ])
            skills_html = f"""
            <div style="margin-bottom: 1.25rem; font-family: {font_family};">
                <h3 style="{section_title_style}">Skills & Technologies</h3>
                <div style="line-height: 1.8;">{skills_pills}</div>
            </div>
            """
        else:
            skills_joined = ", ".join(resume_data.skills)
            skills_html = f"""
            <div style="margin-bottom: 1.25rem; font-family: {font_family};">
                <h3 style="{section_title_style}">Skills</h3>
                <p style="color: #334155; font-size: 0.8rem; margin: 0; line-height: 1.4;">{skills_joined}</p>
            </div>
            """

    # 7. Certifications Section
    certs_html = ""
    if resume_data.certifications:
        certs_entries = []
        for cert in resume_data.certifications:
            if not cert.title:
                continue
            issuer_part = f" by {cert.issuer}" if cert.issuer else ""
            year_part = f" ({cert.year})" if cert.year else ""
            certs_entries.append(f"<li style='margin-bottom: 0.2rem;'><strong>{cert.title}</strong>{issuer_part}{year_part}</li>")
        if certs_entries:
            certs_html = f"""
            <div style="margin-bottom: 1.25rem; font-family: {font_family};">
                <h3 style="{section_title_style}">Certifications</h3>
                <ul style="color: #334155; font-size: 0.8rem; margin: 0; padding-left: 1.2rem; line-height: 1.4;">
                    {"".join(certs_entries)}
                </ul>
            </div>
            """

    # Dedent each block to ensure no Markdown-like indented block formatting occurs
    header_html = textwrap.dedent(header_html).strip()
    summary_html = textwrap.dedent(summary_html).strip()
    exp_html = textwrap.dedent(exp_html).strip()
    edu_html = textwrap.dedent(edu_html).strip()
    proj_html = textwrap.dedent(proj_html).strip()
    skills_html = textwrap.dedent(skills_html).strip()
    certs_html = textwrap.dedent(certs_html).strip()

    # Combine All into a white paper container, completely left-aligned (no tabs/indents)
    sheet_html = f"""<div class="resume-preview-sheet" style="
background: #ffffff !important;
color: #1e293b !important;
font-family: {font_family};
padding: 2.5rem;
border-radius: 8px;
box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
border: 1px solid rgba(0, 0, 0, 0.05);
max-width: 100%;
min-height: 800px;
margin-bottom: 2rem;
text-align: left;
">
{header_html}
{summary_html}
{exp_html}
{edu_html}
{proj_html}
{skills_html}
{certs_html}
</div>"""
    
    st.markdown(sheet_html, unsafe_allow_html=True)
