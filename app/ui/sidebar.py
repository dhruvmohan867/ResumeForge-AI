"""
Sidebar navigation and status panel.

Renders the application sidebar with navigation, premium theme toggle,
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
        <div style="text-align:center; padding:1.5rem 0 2rem 0;">
            <div style="
                display:inline-flex; align-items:center; justify-content:center;
                width:48px; height:48px; border-radius:12px;
                background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1));
                border: 1px solid rgba(99,102,241,0.2);
                font-size:1.5rem; margin-bottom:0.75rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            ">
                {APP_ICON}
            </div>
            <h1 style="
                font-size:1.1rem; font-weight:700; letter-spacing:-0.03em;
                color: var(--text-primary);
                margin:0 0 0.25rem 0;
            ">{APP_NAME}</h1>
            <p style="font-size:0.7rem; color:var(--text-muted); font-weight:500; margin:0;">v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("<p style='font-size:0.65rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;'>Menu</p>", unsafe_allow_html=True)

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

        st.markdown("<hr style='margin: 1.5rem 0; border-color: var(--border-color);'>", unsafe_allow_html=True)

        # Resume completion tracker
        resume_data = get_session(SESSION_RESUME_DATA)
        if resume_data and isinstance(resume_data, ResumeData):
            st.markdown("<p style='font-size:0.65rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;'>Profile Progress</p>", unsafe_allow_html=True)
            render_completion_tracker(resume_data)

            # Quick score
            score = quick_score(resume_data)
            st.markdown(f"""
            <div style="
                display:flex; align-items:center; justify-content:space-between;
                padding:0.875rem 1rem;
                background:var(--input-bg);
                border-radius:8px; margin-top:1rem;
                border:1px solid var(--border-color);
            ">
                <span style="font-size:0.75rem; color:var(--text-secondary); font-weight:500;">Profile Score</span>
                <span style="font-size:1.25rem; font-weight:700; color:var(--accent-color);">{score}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 1.5rem 0; border-color: var(--border-color);'>", unsafe_allow_html=True)

        # Theme toggle (Segmented Control via CSS)
        st.markdown("<p style='font-size:0.65rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;'>Appearance</p>", unsafe_allow_html=True)
        
        current_theme = "Dark" if get_session(SESSION_DARK_MODE, True) else "Light"
        
        theme_choice = st.radio(
            "Appearance",
            options=["Light", "Dark"],
            index=1 if current_theme == "Dark" else 0,
            key="theme_radio",
            label_visibility="collapsed",
            horizontal=True,
        )
        
        is_dark = theme_choice == "Dark"
        if is_dark != get_session(SESSION_DARK_MODE):
            set_session(SESSION_DARK_MODE, is_dark)
            st.rerun()

    return get_session(SESSION_ACTIVE_TAB, NAV_TABS[0][1])
