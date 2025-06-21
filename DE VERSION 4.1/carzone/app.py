import streamlit as st
import os
import sys
import importlib

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Page configuration
st.set_page_config(
    page_title="TechCar2 - Used Car Hub",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the sidebar completely
st.markdown("""
    <style>
    [data-testid="stSidebar"], .css-1lcbmhc.e1fqkh3o3 { display: none !important; }
    .stApp {
        background: #181a20 !important;
        color: #fff !important;
        min-height: 100vh;
    }
    /* Modern Navigation Buttons */
    .nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 48px;
        margin-bottom: 32px;
        padding: 16px 0 16px 0;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    .nav-button {
        padding: 12px 32px;
        font-size: 18px;
        font-weight: 700;
        border: none;
        border-radius: 18px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(.4,0,.2,1);
        background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%);
        color: white;
        box-shadow: 0 6px 24px 0 rgba(33, 150, 243, 0.18), 0 1.5px 6px 0 rgba(156, 39, 176, 0.10);
        outline: none;
    }
    .nav-button:hover, .nav-button.active {
        background: linear-gradient(90deg, #9C27B0 0%, #1976d2 100%);
        box-shadow: 0 8px 32px 0 rgba(156, 39, 176, 0.22), 0 2px 8px 0 rgba(33, 150, 243, 0.12);
        color: #fff;
        transform: translateY(-2px) scale(1.04);
    }
    /* Gradient Card Styles - apply to all card types */
    .tc2-card, .sell-card, .admin-card, .stCard, .card, .nav-container {
        background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) !important;
        color: white !important;
        border-radius: 22px !important;
        box-shadow: 0 6px 32px 0 rgba(33,150,243,0.18), 0 2px 8px 0 rgba(156,39,176,0.10) !important;
        padding: 32px 24px !important;
        margin-bottom: 32px !important;
        transition: box-shadow 0.3s, transform 0.3s !important;
    }
    .tc2-card:hover, .sell-card:hover, .admin-card:hover, .stCard:hover, .card:hover, .nav-container:hover {
        box-shadow: 0 12px 48px 0 rgba(156,39,176,0.22), 0 4px 16px 0 rgba(33,150,243,0.12) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }
    /* Header Styles */
    .tc2-header {
        text-align: center;
        margin-bottom: 32px;
    }
    .tc2-header h1 {
        font-size: 44px;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .tc2-header .car-emoji {
        font-size: 48px;
        margin-right: 18px;
        filter: drop-shadow(0 2px 8px #0008);
    }
    .tc2-header p {
        font-size: 20px;
        opacity: 0.92;
        margin: 0;
    }
    /* Universal Blue-Wine Gradient for All Streamlit Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) !important;
        color: #fff !important;
        font-weight: 700;
        font-size: 17px;
        border: none;
        border-radius: 18px !important;
        box-shadow: 0 4px 16px 0 rgba(33, 150, 243, 0.18), 0 1.5px 6px 0 rgba(156, 39, 176, 0.10);
        padding: 12px 32px !important;
        margin: 6px 0 !important;
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
        outline: none;
    }
    .stButton > button:hover, .stButton > button:active, .stButton > button:focus {
        background: linear-gradient(90deg, #9C27B0 0%, #1976d2 100%) !important;
        color: #fff !important;
        box-shadow: 0 8px 32px 0 rgba(156, 39, 176, 0.22), 0 2px 8px 0 rgba(33, 150, 243, 0.12);
        transform: translateY(-2px) scale(1.04);
    }
    /* Gradient for headers */
    .tc2-header, .sell-header, .admin-header {
        background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) !important;
        color: #fff !important;
        border-radius: 22px !important;
        box-shadow: 0 6px 32px 0 rgba(33,150,243,0.18), 0 2px 8px 0 rgba(156,39,176,0.10) !important;
        padding: 32px 24px !important;
        margin-bottom: 32px !important;
        text-align: center !important;
    }
    /* Gradient for badges and feature tags */
    .tc2-badge, .tc2-feature-badge, .sell-feature-tag {
        background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) !important;
        color: #fff !important;
        font-weight: 700;
        font-size: 20px;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px 0 rgba(33, 150, 243, 0.18), 0 1px 4px 0 rgba(156, 39, 176, 0.10);
        padding: 10px 28px !important;
        margin: 8px 8px 8px 0 !important;
        display: inline-block !important;
        letter-spacing: 1px;
        transition: box-shadow 0.2s, transform 0.2s !important;
        text-align: center;
    }
    .tc2-badge:hover, .tc2-feature-badge:hover, .sell-feature-tag:hover {
        box-shadow: 0 6px 24px 0 rgba(156, 39, 176, 0.22), 0 2px 8px 0 rgba(33, 150, 243, 0.12) !important;
        transform: translateY(-2px) scale(1.04) !important;
    }
    /* Blue-wine gradient border for all Streamlit inputs */
    .stTextInput > div > div > input,
    .stNumberInput input,
    .stNumberInput > div > input,
    .stSelectbox > div[data-baseweb="select"] > div,
    .stMultiSelect > div[data-baseweb="select"] > div,
    .stFileUploader > div {
        border: 2.5px solid;
        border-image: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%) 1;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(33,150,243,0.10), 0 1px 4px rgba(156,39,176,0.10);
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput input:focus,
    .stNumberInput > div > input:focus,
    .stSelectbox > div[data-baseweb="select"] > div:focus-within,
    .stMultiSelect > div[data-baseweb="select"] > div:focus-within,
    .stFileUploader > div:focus-within {
        border-width: 3px;
        border-image: linear-gradient(90deg, #9C27B0 0%, #1976d2 100%) 1;
        box-shadow: 0 4px 16px rgba(156,39,176,0.18), 0 2px 8px rgba(33,150,243,0.12);
    }
    </style>
""", unsafe_allow_html=True)

# Create necessary directories if they don't exist
directories = [
    'pages',
    'utils',
    'model',
    'uploads/images',
    'uploads/documents'
]
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Navigation pages and icons
PAGES = ["Home", "Buy", "Sell", "Estimate", "Admin"]
ICONS = ["🏠", "🚗", "📤", "💰", "🛡️"]
PAGE_MODULES = [None, "pages.Buy", "pages.Sell", "pages.Estimate", "pages.Admin"]

# Initialize session state for navigation
if 'nav_page' not in st.session_state:
    st.session_state['nav_page'] = PAGES[0]

# Horizontal navigation using columns
cols = st.columns(len(PAGES))
for i, (col, page, icon) in enumerate(zip(cols, PAGES, ICONS)):
    with col:
        if st.button(f"{icon} {page}", key=f"nav_{page}"):
            st.session_state['nav_page'] = page
            st.rerun()

# Render the selected page
page = st.session_state['nav_page']
page_idx = PAGES.index(page)
page_module = PAGE_MODULES[page_idx]
if page_module:
    try:
        # Import the module directly
        mod = importlib.import_module(page_module)
        
        # Call main() if it exists
        if hasattr(mod, 'main'):
            mod.main()
        else:
            st.error(f"Page {page} is missing the main() function. Please contact support.")
    except ImportError as e:
        st.error(f"Could not load page {page}: {str(e)}")
    except Exception as e:
        st.error(f"Error in page {page}: {str(e)}")

if page == "Home":
    # Main header
    st.markdown("""
        <div class="tc2-header">
            <h1><span class="car-emoji">🚗</span>TechCar2</h1>
            <p>India's Modern Marketplace for Used Cars</p>
        </div>
    """, unsafe_allow_html=True)

    # Mission, Vision, Benefits Section (show only on Home page)
    st.markdown("""
        <div style="display: flex; gap: 32px; justify-content: center; margin-bottom: 32px;">
            <div style="flex:1; background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%); color: #fff; border-radius: 18px; box-shadow: 0 4px 16px rgba(33,150,243,0.18); padding: 32px 24px; min-width: 260px;">
                <h2 style='margin-top:0;'>🚀 Mission</h2>
                <p style='font-size:17px;'>To empower every Indian to buy and sell used cars with trust, transparency, and technology—making mobility accessible and hassle-free for all.</p>
            </div>
            <div style="flex:1; background: linear-gradient(90deg, #9C27B0 0%, #1976d2 100%); color: #fff; border-radius: 18px; box-shadow: 0 4px 16px rgba(156,39,176,0.18); padding: 32px 24px; min-width: 260px;">
                <h2 style='margin-top:0;'>🌟 Vision</h2>
                <p style='font-size:17px;'>To be India's most trusted, innovative, and customer-centric platform for pre-owned cars, setting new standards in digital automotive experiences.</p>
            </div>
            <div style="flex:1; background: linear-gradient(90deg, #1976d2 0%, #9C27B0 100%); color: #fff; border-radius: 18px; box-shadow: 0 4px 16px rgba(33,150,243,0.18); padding: 32px 24px; min-width: 260px;">
                <h2 style='margin-top:0;'>💡 Benefits</h2>
                <ul style='font-size:17px; padding-left:18px;'>
                    <li>Verified, admin-approved car listings</li>
                    <li>Smart price estimation & transparent deals</li>
                    <li>Secure document uploads & digital process</li>
                    <li>Modern, easy-to-use interface</li>
                    <li>Pan-India coverage</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)
