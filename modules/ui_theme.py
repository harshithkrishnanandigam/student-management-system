# ==============================================================================
# File: modules/ui_theme.py
# Purpose: Minimalist Dark Obsidian & Monochrome UI Theme
# Design Style: High-contrast Dark Monochrome (Inspired by Linear, Vercel & Raycast)
# ==============================================================================

import streamlit as st

def apply_minimal_dark_theme():
    """
    Applies an ultra-clean, minimalist monochrome dark theme.
    Key characteristics:
    - Pitch/obsidian black canvas (#09090b / #000000)
    - Pure white high-contrast action buttons (#ffffff text: #000000)
    - Hairline subtle borders (rgba(255, 255, 255, 0.08))
    - Zero emojis; purely typographic, elegant, and modern
    """
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Canvas */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background-color: #09090b !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(255, 255, 255, 0.02) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(255, 255, 255, 0.015) 0px, transparent 50%) !important;
        color: #f4f4f5 !important;
    }

    /* Minimalist Dark Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0c0c0e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
    }

    /* Sidebar Radio Navigation */
    section[data-testid="stSidebar"] .stRadio > div {
        background-color: transparent !important;
        gap: 4px !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #a1a1aa !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 8px 14px !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
        border: 1px solid transparent !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    section[data-testid="stSidebar"] .stRadio [data-checked="true"] {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    /* Metric Cards (Monochrome High-Contrast) */
    div[data-testid="stMetric"] {
        background-color: #121215 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        transition: border-color 0.2s ease, transform 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(255, 255, 255, 0.18) !important;
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] p {
        color: #71717a !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }

    /* Minimalist Containers & Forms */
    div[data-testid="stForm"], 
    div[data-testid="stContainer"][border="true"] {
        background-color: #121215 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 22px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
    }

    /* Tabs (Monochrome Pill Strip) */
    div[data-baseweb="tab-list"] {
        background-color: #141418 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        display: inline-flex !important;
        gap: 4px !important;
        margin-bottom: 20px !important;
    }

    button[data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        color: #a1a1aa !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #27272a !important;
        color: #ffffff !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3) !important;
    }

    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* High-Contrast Action Buttons (Solid White, Black Text) */
    .stButton > button {
        background-color: #ffffff !important;
        color: #09090b !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        padding: 8px 20px !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1) !important;
    }

    .stButton > button:hover {
        background-color: #e4e4e7 !important;
        border-color: #e4e4e7 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(255, 255, 255, 0.18) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Primary Danger / Delete Button */
    button[kind="primary"] {
        background-color: #27272a !important;
        color: #f87171 !important;
        border: 1px solid #3f3f46 !important;
    }

    button[kind="primary"]:hover {
        background-color: #ef4444 !important;
        color: #ffffff !important;
        border-color: #ef4444 !important;
    }

    /* Form Submit Buttons */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #ffffff !important;
        color: #09090b !important;
        font-weight: 600 !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #f4f4f5 !important;
    }

    /* Inputs, Number Inputs, Selectboxes */
    .stTextInput input, 
    .stNumberInput input, 
    .stDateInput input,
    div[data-baseweb="select"] > div {
        background-color: #141416 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #f4f4f5 !important;
        font-size: 0.9rem !important;
        padding: 9px 12px !important;
        transition: border-color 0.15s ease !important;
    }

    .stTextInput input:focus, 
    .stNumberInput input:focus, 
    .stDateInput input:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 1px #ffffff !important;
    }

    /* Dropdown Menus */
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #141418 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    /* Tables & DataFrames */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        background-color: #121215 !important;
    }

    /* Status Alerts: Refined Minimalist Notices */
    .stAlert {
        background-color: #141418 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #e4e4e7 !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #09090b;
    }
    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)


def render_minimal_header(title: str, subtitle: str = ""):
    """
    Renders an elegant, clean header with zero emojis.
    Pure typography matching modern monochrome interfaces.
    """
    html = f"""
    <div style="
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 16px;
        margin-bottom: 24px;
    ">
        <h1 style="
            margin: 0;
            font-size: 1.6rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.4px;
        ">{title}</h1>
        {f'<p style="margin: 4px 0 0 0; color: #71717a; font-size: 0.88rem; font-weight: 400;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
