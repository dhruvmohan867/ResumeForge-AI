"""
Premium SaaS CSS injection for the Streamlit application.

Provides an advanced dark/light theme system, modern glassmorphism,
smooth animations, custom typography (Inter), and highly polished 
Vercel/Linear-inspired aesthetics.
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
            --bg-primary: #09090b; /* Very dark background */
            --bg-secondary: #18181b;
            --card-bg: rgba(24, 24, 27, 0.6);
            --card-bg-hover: rgba(39, 39, 42, 0.8);
            --border-color: rgba(255, 255, 255, 0.1);
            --border-hover: rgba(255, 255, 255, 0.2);
            --text-primary: #fafafa;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --accent-color: #818cf8;
            --accent-hover: #6366f1;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --input-bg: rgba(255, 255, 255, 0.03);
            --input-border: rgba(255, 255, 255, 0.1);
            --input-focus: rgba(129, 140, 248, 0.5);
            --sidebar-bg: #09090b;
            --shadow-color: rgba(0, 0, 0, 0.5);
            --glass-blur: blur(16px);
        """
    else:
        theme_vars = """
            --bg-primary: #fbfbfc; /* Clean off-white */
            --bg-secondary: #ffffff;
            --card-bg: rgba(255, 255, 255, 0.8);
            --card-bg-hover: rgba(255, 255, 255, 1);
            --border-color: rgba(0, 0, 0, 0.08);
            --border-hover: rgba(0, 0, 0, 0.15);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --accent-color: #4f46e5;
            --accent-hover: #4338ca;
            --success-color: #059669;
            --warning-color: #d97706;
            --error-color: #dc2626;
            --input-bg: rgba(0, 0, 0, 0.015);
            --input-border: rgba(0, 0, 0, 0.1);
            --input-focus: rgba(79, 70, 229, 0.4);
            --sidebar-bg: #f8fafc;
            --shadow-color: rgba(0, 0, 0, 0.04);
            --glass-blur: blur(12px);
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {{
        {theme_vars}
        transition: background-color 0.4s ease, color 0.4s ease;
    }}

    /* ================================================
       GLOBAL RESET & TYPOGRAPHY
    ================================================ */
    *, *::before, *::after {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        box-sizing: border-box;
    }}

    .stApp {{
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}

    p, span, label, div {{
        color: var(--text-secondary);
        line-height: 1.6;
    }}

    /* ================================================
       SIDEBAR
    ================================================ */
    [data-testid="stSidebar"] {{
        background: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 2px 0 20px var(--shadow-color) !important;
    }}

    [data-testid="stSidebar"] > div {{
        padding-top: 1rem !important;
    }}

    /* ================================================
       MAIN CONTENT
    ================================================ */
    .main .block-container {{
        max-width: 1000px !important; /* Slightly narrower for readability */
        padding: 3rem 2.5rem !important;
    }}

    /* ================================================
       INPUT FIELDS
    ================================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 0.95rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) inset !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus-within {{
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 4px var(--input-focus) !important;
        background: transparent !important;
    }}

    .stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {{
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.4rem !important;
    }}

    /* ================================================
       BUTTONS
    ================================================ */
    .stButton > button {{
        border-radius: 8px !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid var(--border-color) !important;
    }}

    /* Primary Buttons */
    .stButton > button[data-testid="baseButton-primary"] {{
        background: var(--text-primary) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        box-shadow: 0 4px 12px var(--shadow-color) !important;
    }}

    .stButton > button[data-testid="baseButton-primary"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px var(--shadow-color) !important;
        opacity: 0.9;
    }}

    /* Secondary Buttons */
    .stButton > button[data-testid="baseButton-secondary"] {{
        background: var(--input-bg) !important;
        color: var(--text-primary) !important;
    }}

    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: var(--card-bg-hover) !important;
        border-color: var(--border-hover) !important;
    }}

    /* ================================================
       CUSTOM THEME TOGGLE (Radio styled as Segmented Control)
    ================================================ */
    div.row-widget.stRadio > div {{
        background: var(--input-bg);
        border: 1px solid var(--input-border);
        border-radius: 9999px;
        padding: 4px;
        display: flex;
        flex-direction: row;
        gap: 4px;
        box-shadow: inset 0 1px 3px var(--shadow-color);
    }}
    div.row-widget.stRadio > div > label {{
        padding: 0;
        margin: 0;
        flex: 1;
        display: flex;
        justify-content: center;
    }}
    div.row-widget.stRadio > div > label > div:first-child {{
        display: none; /* Hide native radio circle */
    }}
    div.row-widget.stRadio > div > label > div:last-child {{
        padding: 0.4rem 1rem !important;
        border-radius: 9999px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        background: transparent !important;
        transition: all 0.3s ease !important;
        width: 100%;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }}
    div.row-widget.stRadio > div > label[data-checked="true"] > div:last-child {{
        background: var(--text-primary) !important;
        color: var(--bg-primary) !important;
        box-shadow: 0 2px 8px var(--shadow-color) !important;
    }}
    div.row-widget.stRadio > div > label:hover > div:last-child {{
        color: var(--text-primary) !important;
    }}

    /* ================================================
       FILE UPLOADER
    ================================================ */
    [data-testid="stFileUploader"] {{
        background: var(--input-bg) !important;
        border: 1px dashed var(--input-border) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: var(--accent-color) !important;
        background: var(--card-bg) !important;
    }}

    /* ================================================
       EXPANDER
    ================================================ */
    .streamlit-expanderHeader {{
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        transition: background 0.2s ease !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: var(--card-bg-hover) !important;
    }}

    .streamlit-expanderContent {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1.5rem !important;
    }}

    /* ================================================
       ALERTS & STATUS
    ================================================ */
    .stSuccess, .stInfo, .stWarning, .stError {{
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 4px 12px var(--shadow-color) !important;
        padding: 1rem 1.25rem !important;
    }}

    /* ================================================
       DIVIDER
    ================================================ */
    hr {{
        border-color: var(--border-color) !important;
        margin: 2.5rem 0 !important;
    }}

    /* ================================================
       ANIMATIONS
    ================================================ */
    @keyframes scorePopIn {{
        0% {{ transform: scale(0.8); opacity: 0; }}
        60% {{ transform: scale(1.02); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}

    @keyframes fadeInUp {{
        from {{ transform: translateY(10px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* Fade-in for main content */
    .main .block-container {{
        animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    /* ================================================
       SCROLLBAR
    ================================================ */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-muted);
    }}

    /* ================================================
       RESPONSIVE
    ================================================ */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1.5rem 1rem !important;
        }}
    }}
    </style>
    """
