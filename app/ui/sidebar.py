"""
Sidebar navigation and status panel.

Renders the application sidebar with navigation, theme toggle,
completion tracker, and quick actions.
"""

from __future__ import annotations

import streamlit as st

from app.config import APP_NAME, APP_VERSION, APP_ICON
from app.models.resume_schema import ResumeData
from app.utils.constants import (
    NAV_TABS,
    SESSION_ACTIVE_TAB,
    SESSION_DARK_MODE,
    SESSION_RESUME_DATA,
)
from app.utils.helpers import init_session_state, get_session, set_session
from app.ui.components import render_completion_tracker
from app.services.ats_service import quick_score


def render_sidebar() -> str:
    """
    Render the sidebar and return the selected tab name.
    
    Returns:
        The currently active tab name (e.g. "Resume Builder")
    """
    init_session_state(SESSION_ACTIVE_TAB, NAV_TABS[0][1])
    init_session_state(SESSION_DARK_MODE, True)

    with st.sidebar:
        # App branding
        st.markdown(f"""
        <div style="text-align:center; padding:1rem 0 1.5rem 0;">
            <span style="font-size:2.5rem;">{APP_ICON}</span>
            <h1 style="
                font-size:1.3rem; font-weight:800;
                background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin:0.3rem 0 0 0;
            ">{APP_NAME}</h1>
            <p style="font-size:0.7rem; color:var(--text-muted,#64748b); margin:0;">v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        st.markdown("<p style='font-size:0.7rem; font-weight:600; color:var(--text-muted,#64748b); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.5rem;'>Navigation</p>", unsafe_allow_html=True)

        for icon, tab_name in NAV_TABS:
            is_active = get_session(SESSION_ACTIVE_TAB) == tab_name
            if st.button(
                f"{icon}  {tab_name}",
                key=f"nav_{tab_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                set_session(SESSION_ACTIVE_TAB, tab_name)
                st.rerun()

        st.markdown("---")

        # Resume completion tracker
        resume_data = get_session(SESSION_RESUME_DATA)
        if resume_data and isinstance(resume_data, ResumeData):
            st.markdown("<p style='font-size:0.7rem; font-weight:600; color:var(--text-muted,#64748b); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.5rem;'>Progress</p>", unsafe_allow_html=True)
            render_completion_tracker(resume_data)

            # Quick score
            score = quick_score(resume_data)
            st.markdown(f"""
            <div style="
                text-align:center; padding:0.75rem;
                background:rgba(99,102,241,0.1);
                border-radius:12px; margin-top:0.75rem;
                border:1px solid rgba(99,102,241,0.2);
            ">
                <p style="font-size:0.65rem; color:var(--text-muted,#64748b); margin:0; text-transform:uppercase; letter-spacing:1px;">Quick Score</p>
                <p style="font-size:1.8rem; font-weight:800; color:#6366f1; margin:0;">{score}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Theme toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=get_session(SESSION_DARK_MODE, True), key="theme_toggle")
        set_session(SESSION_DARK_MODE, dark_mode)

    return get_session(SESSION_ACTIVE_TAB, NAV_TABS[0][1])
