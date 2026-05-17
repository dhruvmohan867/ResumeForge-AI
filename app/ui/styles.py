"""
Modern SaaS CSS injection for the Streamlit application.

Provides dark/light theme support, glassmorphism cards,
smooth animations, custom typography, and responsive layout.
"""

from __future__ import annotations


def get_custom_css(dark_mode: bool = True) -> str:
    """
    Generate the complete custom CSS for the application.
    
    Args:
        dark_mode: Whether to use dark theme variables
        
    Returns:
        CSS string wrapped in <style> tags
    """
    if dark_mode:
        theme_vars = """
            --bg-primary: #0f0f1a;
            --bg-secondary: #161625;
            --card-bg: rgba(22, 22, 37, 0.9);
            --card-bg-hover: rgba(30, 30, 50, 0.95);
            --border-color: rgba(255, 255, 255, 0.06);
            --border-hover: rgba(99, 102, 241, 0.3);
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-color: #6366f1;
            --accent-hover: #818cf8;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --input-bg: rgba(255, 255, 255, 0.04);
            --input-border: rgba(255, 255, 255, 0.08);
            --input-focus: rgba(99, 102, 241, 0.4);
            --sidebar-bg: #0d0d1a;
            --shadow-color: rgba(0, 0, 0, 0.3);
        """
    else:
        theme_vars = """
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --card-bg: rgba(255, 255, 255, 0.95);
            --card-bg-hover: rgba(255, 255, 255, 1);
            --border-color: rgba(0, 0, 0, 0.06);
            --border-hover: rgba(99, 102, 241, 0.3);
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --accent-color: #6366f1;
            --accent-hover: #4f46e5;
            --success-color: #059669;
            --warning-color: #d97706;
            --error-color: #dc2626;
            --input-bg: rgba(0, 0, 0, 0.02);
            --input-border: rgba(0, 0, 0, 0.1);
            --input-focus: rgba(99, 102, 241, 0.4);
            --sidebar-bg: #f1f5f9;
            --shadow-color: rgba(0, 0, 0, 0.08);
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
    }}

    /* ================================================
       GLOBAL RESET & TYPOGRAPHY
    ================================================ */
    *, *::before, *::after {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .stApp {{
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }}

    p, span, label, div {{
        color: var(--text-secondary);
    }}

    /* ================================================
       SIDEBAR
    ================================================ */
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color) !important;
    }}

    [data-testid="stSidebar"] > div {{
        padding-top: 0.5rem !important;
    }}

    /* ================================================
       MAIN CONTENT
    ================================================ */
    .main .block-container {{
        max-width: 1100px !important;
        padding: 2rem 2.5rem !important;
    }}

    /* ================================================
       INPUT FIELDS
    ================================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 0.6rem 0.8rem !important;
        transition: all 0.2s ease !important;
        font-size: 0.9rem !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--input-focus) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
    }}

    .stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {{
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}

    /* ================================================
       BUTTONS
    ================================================ */
    .stButton > button {{
        border-radius: 10px !important;
        padding: 0.55rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.25s ease !important;
        border: 1px solid var(--border-color) !important;
    }}

    .stButton > button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
    }}

    .stButton > button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }}

    .stButton > button[data-testid="baseButton-secondary"] {{
        background: var(--input-bg) !important;
        color: var(--text-secondary) !important;
    }}

    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: var(--card-bg-hover) !important;
        border-color: var(--border-hover) !important;
        color: var(--accent-color) !important;
    }}

    /* ================================================
       FILE UPLOADER
    ================================================ */
    [data-testid="stFileUploader"] {{
        background: var(--input-bg) !important;
        border: 2px dashed var(--input-border) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease !important;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: var(--accent-color) !important;
    }}

    /* ================================================
       EXPANDER
    ================================================ */
    .streamlit-expanderHeader {{
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}

    .streamlit-expanderContent {{
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }}

    /* ================================================
       DOWNLOAD BUTTON
    ================================================ */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
    }}

    .stDownloadButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }}

    /* ================================================
       ALERTS & STATUS
    ================================================ */
    .stSuccess, .stInfo, .stWarning, .stError {{
        border-radius: 10px !important;
        border: none !important;
    }}

    /* ================================================
       TOGGLE
    ================================================ */
    .stToggle label span {{
        color: var(--text-secondary) !important;
    }}

    /* ================================================
       DIVIDER
    ================================================ */
    hr {{
        border-color: var(--border-color) !important;
    }}

    /* ================================================
       ANIMATIONS
    ================================================ */
    @keyframes scorePopIn {{
        0% {{ transform: scale(0.5); opacity: 0; }}
        70% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    @keyframes fadeInUp {{
        from {{ transform: translateY(15px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* Fade-in for main content */
    .main .block-container {{
        animation: fadeInUp 0.4s ease-out !important;
    }}

    /* ================================================
       SCROLLBAR
    ================================================ */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-muted);
    }}

    /* ================================================
       RESPONSIVE
    ================================================ */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem 1rem !important;
        }}
    }}
    </style>
    """
