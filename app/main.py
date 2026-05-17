"""
ResumeForge AI — Main Application Entry Point.

This is the Streamlit application root. It:
1. Configures the page
2. Initializes session state
3. Injects custom CSS
4. Renders the sidebar
5. Routes to the active tab
"""

from __future__ import annotations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.config import APP_NAME, APP_ICON, APP_DESCRIPTION
from app.models.resume_schema import ResumeData
from app.utils.constants import (
    SESSION_RESUME_DATA,
    SESSION_ATS_RESULT,
    SESSION_DARK_MODE,
    SESSION_SELECTED_TEMPLATE,
    SESSION_ACTIVE_TAB,
    SESSION_TOAST_QUEUE,
)
from app.utils.helpers import init_session_state, get_session, flush_toasts
from app.ui.styles import get_custom_css
from app.ui.sidebar import render_sidebar
from app.ui.dashboard import (
    render_builder_tab,
    render_upload_tab,
    render_ats_tab,
    render_enhance_tab,
    render_export_tab,
)
from app.database.db import init_db


def main() -> None:
    """Application entry point."""

    # Page configuration
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": f"### {APP_ICON} {APP_NAME}\n{APP_DESCRIPTION}\n\nBuilt with Streamlit & OpenAI",
        },
    )

    # Initialize session state defaults
    _init_session_defaults()

    # Initialize database
    init_db()

    # Inject custom CSS
    dark_mode = get_session(SESSION_DARK_MODE, True)
    st.markdown(get_custom_css(dark_mode), unsafe_allow_html=True)

    # Flush queued toast notifications
    flush_toasts()

    # Render sidebar and get active tab
    active_tab = render_sidebar()

    # Route to active tab
    tab_routes = {
        "Resume Builder": render_builder_tab,
        "Upload & Parse": render_upload_tab,
        "ATS Analysis": render_ats_tab,
        "AI Enhance": render_enhance_tab,
        "Export PDF": render_export_tab,
    }

    renderer = tab_routes.get(active_tab, render_builder_tab)
    renderer()

    # Footer
    st.markdown("""
    <div style="
        text-align:center; padding:2rem 0 1rem 0;
        border-top:1px solid var(--border-color, rgba(255,255,255,0.06));
        margin-top:3rem;
    ">
        <p style="font-size:0.75rem; color:var(--text-muted,#64748b);">
            ⚡ Powered by <strong style="color:var(--accent-color,#6366f1);">ResumeForge AI</strong> 
            — Built with Streamlit & OpenAI
        </p>
    </div>
    """, unsafe_allow_html=True)


def _init_session_defaults() -> None:
    """Initialize all session state keys with defaults."""
    init_session_state(SESSION_RESUME_DATA, ResumeData())
    init_session_state(SESSION_ATS_RESULT, None)
    init_session_state(SESSION_DARK_MODE, True)
    init_session_state(SESSION_SELECTED_TEMPLATE, "tech_minimalist")
    init_session_state(SESSION_ACTIVE_TAB, "Resume Builder")
    init_session_state(SESSION_TOAST_QUEUE, [])


if __name__ == "__main__":
    main()
