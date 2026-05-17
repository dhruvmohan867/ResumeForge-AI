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
