"""
Reusable UI components for the application.

Contains styled cards, score displays, loading states,
toast handlers, and other visual building blocks.
"""

from __future__ import annotations

import streamlit as st

from app.utils.helpers import format_score_color, format_score_label


def render_score_ring(score: int, label: str, size: int = 120) -> None:
    """Render an animated circular score indicator."""
    color = format_score_color(score)
    grade = format_score_label(score)

    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; padding:1rem;">
        <div style="
            width:{size}px; height:{size}px;
            border-radius:50%;
            background: conic-gradient({color} {score * 3.6}deg, rgba(255,255,255,0.1) {score * 3.6}deg);
            display:flex; align-items:center; justify-content:center;
            box-shadow: 0 0 20px {color}33;
            animation: scorePopIn 0.6s ease-out;
        ">
            <div style="
                width:{size - 16}px; height:{size - 16}px;
                border-radius:50%;
                background: var(--card-bg, #1a1a2e);
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
            ">
                <span style="font-size:1.8rem; font-weight:700; color:{color};">{score}</span>
                <span style="font-size:0.65rem; color:var(--text-secondary, #94a3b8); text-transform:uppercase; letter-spacing:1px;">{label}</span>
            </div>
        </div>
        <span style="margin-top:0.5rem; font-size:0.8rem; font-weight:600; color:{color};">{grade}</span>
    </div>
    """, unsafe_allow_html=True)


def render_metric_bar(label: str, value: int, max_value: int = 100) -> None:
    """Render a horizontal progress bar with label."""
    color = format_score_color(value)
    pct = min(value / max_value * 100, 100)

    st.markdown(f"""
    <div style="margin-bottom:0.75rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <span style="font-size:0.8rem; color:var(--text-secondary, #94a3b8);">{label}</span>
            <span style="font-size:0.8rem; font-weight:600; color:{color};">{value}%</span>
        </div>
        <div style="
            height:6px; border-radius:3px;
            background:rgba(255,255,255,0.08);
            overflow:hidden;
        ">
            <div style="
                height:100%; width:{pct}%;
                border-radius:3px;
                background: linear-gradient(90deg, {color}cc, {color});
                transition: width 0.8s ease-out;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_tag_list(tags: list[str], color: str = "#10b981", label: str = "") -> None:
    """Render a list of tags/chips."""
    if not tags:
        return
    if label:
        st.markdown(f"<p style='font-size:0.8rem; color:var(--text-secondary,#94a3b8); margin-bottom:0.3rem;'>{label}</p>", unsafe_allow_html=True)

    tags_html = " ".join([
        f"<span style='display:inline-block; padding:0.2rem 0.6rem; margin:0.15rem; "
        f"border-radius:12px; font-size:0.75rem; font-weight:500; "
        f"background:{color}22; color:{color}; border:1px solid {color}44;'>{t}</span>"
        for t in tags
    ])
    st.markdown(f"<div style='line-height:2;'>{tags_html}</div>", unsafe_allow_html=True)


def render_glass_card(content_html: str, padding: str = "1.5rem") -> None:
    """Render a glassmorphism-styled card."""
    st.markdown(f"""
    <div style="
        background: var(--card-bg, rgba(26,26,46,0.8));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-color, rgba(255,255,255,0.08));
        border-radius: 16px;
        padding: {padding};
        margin-bottom: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    ">
        {content_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(icon: str, title: str, subtitle: str = "") -> None:
    """Render a styled section header."""
    sub_html = f"<p style='font-size:0.85rem; color:var(--text-secondary,#94a3b8); margin:0;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom:1rem;">
        <h2 style="
            font-size:1.4rem; font-weight:700;
            color:var(--text-primary, #e2e8f0);
            margin:0 0 0.25rem 0;
        ">{icon} {title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_enhancement_diff(original: str, enhanced: str, changes: list[str]) -> None:
    """Show a before/after comparison for AI enhancements."""
    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin:1rem 0;">
        <div style="padding:1rem; border-radius:12px; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);">
            <p style="font-size:0.75rem; font-weight:600; color:#ef4444; margin-bottom:0.5rem; text-transform:uppercase;">Original</p>
            <p style="font-size:0.85rem; color:var(--text-secondary,#94a3b8);">""" + original.replace('\n', '<br>') + """</p>
        </div>
        <div style="padding:1rem; border-radius:12px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);">
            <p style="font-size:0.75rem; font-weight:600; color:#10b981; margin-bottom:0.5rem; text-transform:uppercase;">Enhanced</p>
            <p style="font-size:0.85rem; color:var(--text-primary,#e2e8f0);">""" + enhanced.replace('\n', '<br>') + """</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if changes:
        with st.expander("📝 Changes Made"):
            for change in changes:
                st.markdown(f"- {change}")


def render_loading_skeleton(lines: int = 3) -> None:
    """Render a loading skeleton placeholder."""
    skeleton_lines = ""
    for i in range(lines):
        width = 100 - (i * 15)
        skeleton_lines += f"""
        <div style="
            height:12px; width:{width}%;
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%);
            background-size: 200% 100%;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            animation: shimmer 1.5s infinite;
        "></div>
        """
    st.markdown(f"""
    <div style="padding:1rem;">
        {skeleton_lines}
    </div>
    <style>
    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}
    </style>
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
    <div style="margin-bottom:1rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span style="font-size:0.75rem; font-weight:600; color:var(--text-secondary,#94a3b8);">COMPLETION</span>
            <span style="font-size:0.75rem; font-weight:700; color:var(--accent-color,#6366f1);">{pct}%</span>
        </div>
        <div style="height:4px; border-radius:2px; background:rgba(255,255,255,0.06);">
            <div style="height:100%; width:{pct}%; border-radius:2px; background:linear-gradient(90deg,#6366f1,#8b5cf6); transition:width 0.5s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for name, done in sections.items():
        icon = "✅" if done else "⬜"
        color = "var(--text-primary,#e2e8f0)" if done else "var(--text-muted,#64748b)"
        st.markdown(f"<p style='font-size:0.8rem; color:{color}; margin:0.15rem 0;'>{icon} {name}</p>", unsafe_allow_html=True)
