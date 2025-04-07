"""
UI Components module for the Diabetes Nutrition Plan application.
Contains functions for creating and managing the user interface.
"""
import streamlit as st

def show_header():
    """
    Display the application header.
    """
    import streamlit as st
    
    # Check if genetic data is available to customize the header
    has_genetic_data = 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None
    
    if (has_genetic_data):
        st.markdown('<h2 style="color:var(--primary-color); font-size:35px; font-weight:600;">Genetically Optimized Diabetes Nutrition Plan</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:var(--text-muted); font-size:18px;">Personalized nutrition recommendations based on your health metrics, socioeconomic context, and genetic profile</p>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color:var(--primary-color); font-size:35px; font-weight:600;">Personalized Diabetes Nutrition Plan</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:var(--text-muted); font-size:18px;">Personalized nutrition recommendations based on your health metrics and socioeconomic context</p>', unsafe_allow_html=True)

def apply_custom_css():
    """
    Apply custom CSS styling to the application.
    """
    st.markdown("""
    <style>
        /* === GLOBAL STYLES === */
        /* Font styles and base elements */
        :root {
            --primary-color: #5cacee;
            --secondary-color: #1e90ff;
            --accent-color: #f0f8ff;
            --warning-color: #ffb300;
            --success-color: #4CAF50;
            --info-color: #5BC0DE;
            --text-color: #333333;
            --text-muted: #777777;
            --light-bg: #f9f9f9;
            --card-bg: #FFFFFF;
            --border-radius: 10px;
            --box-shadow: 0 2px 5px rgba(255, 255, 255, 0.3);
            --transition: all 0.3s ease;
        }

        /* Typography */
        body {
            font-family: 'Roboto', sans-serif;
            color: var(--text-color);
            line-height: 1.6;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        p {
            margin-bottom: 1rem;
            line-height: 1.6;
        }

        /* === LAYOUT & STRUCTURE === */
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none !important;}
        
        /* Force the entire app to take full height */
        .stApp {
            margin-top: -4rem !important;
        }
        
        /* App container settings */
        .appview-container {
            padding-top: 0 !important;
        }
        
        /* Sidebar adjustments */
        section[data-testid="stSidebar"] {
            top: 0 !important;
            padding-top: 4rem !important;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--input-border);
        }
        
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 4rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ensure proper overflow handling */
        body {
            overflow-x: hidden;
        }
        
        /* === TABS & NAVIGATION === */
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 16px 24px;
            background-color: #f5f5f5;
            color: #555555;
            border-radius: 10px 10px 0px 0px;
            border: none;
            font-weight: 500;
            transition: var(--transition);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
            margin-right: 6px;
            font-size: 1.05rem;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            background-color: #f9f9f9;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 600;
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }
        
        /* Fix spacing around tab panels */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 20px !important;
        }
        
        .stTabs [data-baseweb="tab-content"] {
            padding: 0px !important;
        }
        
        /* === CARDS & CONTAINERS === */
        /* Card styling */
        .card-container {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 24px;
            margin-bottom: 24px;
            border-top: 4px solid var(--primary-color);
        }
        
        /* Plan header */
        .plan-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 24px;
            border-radius: var(--border-radius);
            color: white;
            margin-bottom: 24px;
            text-align: center;
            box-shadow: var(--box-shadow);
        }
        
        /* Plan sections */
        .plan-section {
            background-color: var(--card-bg);
            padding: 24px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            margin-bottom: 24px;
            border-left: 4px solid var(--primary-color);
        }
        
        .plan-section h3 {
            color: var(--primary-color);
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        /* Meal cards */
        .meal-card {
            border: 1px solid var(--input-border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: var(--accent-color);
            transition: var(--transition);
        }
        
        .meal-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .meal-title {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 12px;
            font-size: 1.1rem;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 8px;
        }
        
        /* Foods limit section */
        .limit-section {
            background-color: #FFF8E1;
            border-left: 4px solid #FFC107;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .limit-section h2 {
            color: #FF6F00;
            font-weight: 600;
        }
        
        /* === HEALTH ASSESSMENT STYLING === */
        /* Assessment sections */
        .health-assessment-section {
            margin-bottom: 28px;
            padding: 24px;
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }
        
        .health-assessment-section h2 {
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-top: 0;
            margin-bottom: 16px;
            border-bottom: 2px solid #E8F5E9;
            padding-bottom: 10px;
        }
        
        .health-assessment-section h3 {
            font-size: 1.25rem;
            color: var(--secondary-color);
            margin-top: 16px;
            margin-bottom: 12px;
        }
        
        /* Color-coded assessment sections */
        .summary-section {
            background-color: #E8F5E9;
            border-left: 5px solid var(--primary-color);
        }
        
        .diabetes-management-section {
            background-color: #E3F2FD;
            border-left: 5px solid var(--secondary-color);
        }
        
        .risks-section {
            background-color: #FFEBEE;
            border-left: 5px solid var(--warning-color);
        }
        
        .care-plans-section {
            background-color: #E0F7FA;
            border-left: 5px solid #00BCD4;
        }
        
        .concerns-section {
            background-color: #FFF3E0;
            border-left: 5px solid #FFB74D;
        }
        
        .recommendations-section {
            background-color: #F1F8E9;
            border-left: 5px solid #8BC34A;
        }
        
        .genetic-section {
            background-color: #E8EAF6;
            border-left: 5px solid #3F51B5;
        }
        
        /* === BUTTONS & INTERACTIVE ELEMENTS === */
        /* Button styling */
        .stButton button {
            border-radius: 50px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            transition: var(--transition) !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
        }
        
        /* Primary button */
        .stButton button[kind="primary"] {
            background-color: var(--primary-color) !important;
            border: none !important;
        }
        
        /* Secondary button */
        .stButton button[kind="secondary"] {
            border: 2px solid var(--primary-color) !important;
            color: var(--primary-color) !important;
            background-color: transparent !important;
        }
        
        /* Success message */
        .success-message {
            padding: 16px;
            border-radius: var(--border-radius);
            animation: fadeIn 0.5s ease-in-out;
            border-left: 4px solid var(--success-color);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* === DATA INPUT ELEMENTS === */
        /* Input fields */
        .stTextInput > div > div {
            border-radius: 8px !important;
        }
        
        .stTextInput > div > div:focus-within {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(94, 96, 206, 0.2) !important;
        }
        
        /* Select boxes */
        .stSelectbox > div > div > div {
            border-radius: 8px !important;
        }
        
        .stSelectbox > div > div > div:focus-within {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(94, 96, 206, 0.2) !important;
        }
        
        /* Number inputs */
        .stNumberInput > div > div {
            border-radius: 8px !important;
        }
        
        .stNumberInput > div > div:focus-within {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(94, 96, 206, 0.2) !important;
        }
        
        /* Override Streamlit's default accent colors for form elements */
        /* These override Streamlit's default blue focus colors */
        [data-baseweb="select"] [data-baseweb="tag"] {
            background-color: var(--primary-color) !important;
        }
        
        [data-baseweb="base-input"] {
            border-color: var(--primary-color) !important;
        }
        
        /* Radio buttons */
        [data-baseweb="radio"] [data-checked="true"] {
            color: var(--primary-color) !important;
        }
        
        /* Checkboxes */
        [data-baseweb="checkbox"] [data-checked="true"] {
            background-color: var(--primary-color) !important;
        }
        
        /* Slider */
        [data-testid="stSlider"] > div > div > div {
            background-color: var(--primary-color) !important;
        }
        
        /* === GENETIC DATA VISUALIZATION === */
        /* Genetic badge */
        .genetic-badge {
            background-color: #FAFAFA;
            padding: 10px 16px;
            border-radius: 50px;
            display: inline-flex;
            align-items: center;
            margin-bottom: 1rem;
            border: 1px solid #f0f0f0;
        }
        
        .genetic-badge .icon {
            font-size: 1.2rem;
            margin-right: 8px;
        }
        
        .genetic-badge .text {
            font-weight: 600;
            color: var(--primary-color);
        }
        
        /* Marker cards */
        .marker-card {
            background-color: #FFFFFF;
            border-radius: var(--border-radius);
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid #f0f0f0;
        }
        
        .marker-card .title {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        /* === CUSTOM SIDEBAR NAVIGATION === */
        
        /* Main sidebar styling */
        section[data-testid="stSidebar"] {
            background: var(--sidebar-bg);
            border-right: none;
        }
        
        /* Navigation radio button styling */
        .stRadio > div {
            gap: 10px !important;
            display: flex;
            flex-direction: column;
        }
        
        .stRadio > div > label {
            padding: 16px !important;
            margin: 5px 10px !important;
            border-radius: 16px !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            background-color: var(--sidebar-element-bg) !important;
            color: var(--sidebar-element-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
            font-weight: 500 !important;
            box-shadow: var(--box-shadow) !important;
            position: relative;
            overflow: hidden;
        }
        
        .stRadio > div > label:hover {
            transform: translateY(-3px) !important;
            box-shadow: var(--box-shadow-hover) !important;
        }
        
        .stRadio > div > label:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, rgba(94, 96, 206, 0), rgba(94, 96, 206, 0.1));
            transform: translateX(-100%);
            transition: transform 0.5s ease;
        }
        
        .stRadio > div > label:hover:before {
            transform: translateX(0);
        }
        
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label {
            background: var(--sidebar-element-active-bg) !important;
            color: var(--sidebar-element-active-color) !important;
            font-weight: 600 !important;
            box-shadow: var(--box-shadow-hover) !important;
            border: none !important;
        }
        
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label:after {
            content: "";
            position: absolute;
            top: 12px;
            right: 12px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: rgba(94, 96, 206, 0.7);
            box-shadow: 0 0 5px 2px rgba(94, 96, 206, 0.3);
        }
        
        /* Make radio buttons fit better in sidebar */
        .stRadio [data-testid="stMarkdownContainer"] {
            font-size: 16px !important;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Hide the actual radio button circle and only keep the label */
        .stRadio [data-baseweb="radio"] [data-testid="stRadio"] {
            display: none !important;
        }
        
        /* Add a subtle pulsing glow effect to active menu item */
        @keyframes pulse-glow {
            0% { box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3); }
            50% { box-shadow: 0 5px 20px rgba(46, 125, 50, 0.5); }
            100% { box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3); }
        }
        
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label {
            animation: pulse-glow 2s infinite;
        }
        
        /* Sidebar section header */
        .sidebar-section {
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .sidebar-section h3 {
            font-size: 14px;
            color: var(--sidebar-accent-color);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-left: 15px;
        }
        
        /* Info card in sidebar */
        .sidebar-info-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 18px;
            margin: 15px 10px;
            border: 1px solid #f0f0f0;
            box-shadow: var(--box-shadow);
        }
        
        .sidebar-info-card h4 {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--sidebar-accent-color);
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        .sidebar-info-card p {
            font-size: 14px;
            color: var(--sidebar-text-color);
            margin-bottom: 10px;
            line-height: 1.5;
        }
        
        .sidebar-info-card ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .sidebar-info-card li {
            font-size: 14px;
            margin-bottom: 8px;
            color: var(--sidebar-text-color);
        }
        
        /* Footer section */
        .sidebar-footer {
            margin-top: 30px;
            padding: 12px 10px;
            text-align: center;
            font-size: 13px;
            color: var(--sidebar-text-color);
            background-color: var(--sidebar-element-bg);
            border-radius: 10px;
            margin: 30px 10px 20px 10px;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        /* Genetics badge */
        .genetics-active-badge {
            background: #FAFAFA;
            border-radius: 12px;
            padding: 18px;
            margin: 20px 10px;
            color: var(--sidebar-element-color);
            text-align: center;
            border: 1px solid #f0f0f0;
            position: relative;
            overflow: hidden;
            box-shadow: var(--box-shadow);
        }
        
        .genetics-active-badge:before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 159, 28, 0.15) 0%, rgba(255, 159, 28, 0) 70%);
            opacity: 0;
            animation: ripple 3s infinite ease-out;
        }
        
        @keyframes ripple {
            0% { transform: scale(0.3); opacity: 0; }
            40% { opacity: 0.5; }
            100% { transform: scale(1); opacity: 0; }
        }
        
        .genetics-active-badge .icon {
            font-size: 32px;
            margin-bottom: 12px;
            color: var(--primary-color);
        }
        
        .genetics-active-badge .title {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 5px;
            letter-spacing: 0.5px;
            color: var(--sidebar-element-color);
        }
        
        .genetics-active-badge .subtitle {
            font-size: 12px;
            color: var(--sidebar-element-color);
            background: #f5f5f5;
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            margin-top: 5px;
        }
        
        /* === RESPONSIVE LAYOUT === */
        /* Media queries for different screen sizes */
        @media (max-width: 768px) {
            .health-assessment-section {
                padding: 16px;
            }
            
            .health-assessment-section h2 {
                font-size: 1.3rem;
            }
            
            .plan-section {
                padding: 16px;
            }
            
            .stButton button {
                width: 100%;
            }
        }
        
        @media (max-width: 576px) {
            .meal-card {
                padding: 12px;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 8px 12px;
                font-size: 0.9rem;
            }
            
            .stTabs [data-baseweb="tab-panel"] {
                padding-top: 12px !important;
            }
        }
        
        /* === MODE ADAPTIVE COLORS === */
        /* Light mode (default) - set light theme variables */
        :root {
            /* Light theme variables */
            /* Override the main root variables for light mode */
            --primary-color: #5cacee;
            --secondary-color: #1e90ff;
            --accent-color: #f0f8ff;
            --text-color: #333333;
            --text-muted: #777777;
            
            /* Additional light theme variables */
            --bg-primary: #f9f9f9;
            --bg-secondary: #f0f8ff;
            --card-bg: #ffffff;
            --sidebar-bg: linear-gradient(180deg, #f0f8ff 0%, #e6f2ff 100%);
            --sidebar-element-bg: #FFFFFF;
            --sidebar-element-active-bg: linear-gradient(135deg, #5cacee, #1e90ff);
            --sidebar-element-active-color: #ffffff;
            --sidebar-element-color: #333333;
            --sidebar-text-color: #333333;
            --sidebar-accent-color: #1e90ff;
            --sidebar-badge-bg: rgba(92, 172, 238, 0.1);
            --heading-color: #1e90ff;
            --input-bg: #ffffff;
            --input-border: #e6f2ff;
            --input-text: #333333;
            --button-primary-bg: #5cacee;
            --box-shadow: 0 2px 5px rgba(255, 255, 255, 0.3);
            --box-shadow-hover: 0 4px 8px rgba(255, 255, 255, 0.5);
        }
        
        /* Dark mode - override variables */
        @media (prefers-color-scheme: dark) {
            :root {
                /* Dark theme variables */
                /* Override the main root variables for dark mode */
                --primary-color: #61d46d;
                --secondary-color: #4caf50;
                --accent-color: #1e3e20;
                --text-color: #d1d5db;
                --text-muted: #bdbdbd;
                
                /* Additional dark theme variables */
                --bg-primary: #303030;
                --bg-secondary: #4a5568;
                --card-bg: #424242;
                --sidebar-bg: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
                --sidebar-element-bg: rgba(255, 255, 255, 0.1);
                --sidebar-element-active-bg: linear-gradient(135deg, #61d46d, #4caf50);
                --sidebar-element-active-color: #212121;
                --sidebar-element-color: #ffffff;
                --sidebar-text-color: rgba(255, 255, 255, 0.85);
                --sidebar-accent-color: #61d46d;
                --sidebar-badge-bg: rgba(97, 212, 109, 0.2);
                --heading-color: #61d46d;
                --input-bg: #4a5568;
                --input-border: #2d3748;
                --input-text: #e0e0e0;
                --button-primary-bg: #4caf50;
                --box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
                --box-shadow-hover: 0 6px 12px rgba(255, 255, 255, 0.3);
            }
            
            /* Apply dark mode styles to main elements */
            body {
                background-color: var(--bg-primary);
                color: var(--text-color);
            }
            
            .main .block-container {
                background-color: var(--bg-primary);
            }
            
            /* Tab styling in dark mode */
            .stTabs [data-baseweb="tab"] {
                background-color: var(--bg-secondary);
                color: var(--text-muted);
            }
            
            .stTabs [aria-selected="true"] {
                background: var(--sidebar-element-active-bg) !important;
                color: var(--sidebar-element-active-color) !important;
            }
            
            /* Content containers in dark mode */
            .meal-card {
                background-color: var(--bg-secondary);
                border-color: var(--input-border);
            }
            
            .plan-section {
                background-color: var(--bg-secondary);
                border-left: 4px solid var(--sidebar-accent-color);
            }
            
            .health-assessment-section {
                background-color: var(--bg-secondary);
            }
            
            .marker-card {
                background-color: var(--bg-secondary);
            }
            
            /* Input field styling in dark mode */
            input, select, textarea {
                background-color: var(--input-bg) !important;
                color: var(--input-text) !important;
                border-color: var(--input-border) !important;
            }
            
            .stTextInput > div > div,
            .stSelectbox > div > div > div,
            .stNumberInput > div > div {
                background-color: var(--input-bg) !important;
                border-color: var(--input-border) !important;
            }
            
            /* UI element colors in dark mode */
            [data-testid="stMetricLabel"] {
                color: var(--text-color) !important;
            }
            
            [data-testid="stExpander"] {
                background-color: var(--bg-secondary) !important;
                border-color: var(--input-border) !important;
            }
            
            /* Message styling in dark mode */
            .stSuccess {
                background-color: rgba(94, 96, 206, 0.1) !important;
                color: #b0b1e8 !important;
            }
            
            .stWarning {
                background-color: rgba(255, 159, 28, 0.1) !important;
                color: #ffcf8c !important;
            }
            
            .stInfo {
                background-color: rgba(100, 223, 223, 0.1) !important;
                color: #a0e9e9 !important;
            }
            
            /* Metric value styling */
            [data-testid="stMetricValue"] {
                color: var(--heading-color) !important;
                font-weight: 600 !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    """
    Configure and display the sidebar. Returns the current page selection.
    """
    # Initialize the page state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state.page = "Input Data"
    
    # Check for navigation request flag
    if 'nav_to_input' in st.session_state and st.session_state.nav_to_input:
        st.session_state.page = "Input Data"
        # Clear the flag
        st.session_state.nav_to_input = False
    
    # Navigation items with improved icons
    nav_items = [
        {"id": "Input Data", "icon": "📊", "text": "Input Data"},
        {"id": "Nutrition Plan", "icon": "🍽️", "text": "Nutrition Plan"},
        {"id": "Health Assessment", "icon": "💉", "text": "Health Assessment"},
        {"id": "Educational Resources", "icon": "📚", "text": "Resources"}
    ]
    
    # Add spacing for better layout
    st.sidebar.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    # Instead of custom HTML navigation, use direct radio buttons with styling
    selected_page = st.sidebar.radio(
        "Navigation", 
        [item["id"] for item in nav_items],
        index=[item["id"] for item in nav_items].index(st.session_state.page),
        key="navigation_radio",
        format_func=lambda x: f"{nav_items[[item['id'] for item in nav_items].index(x)]['icon']} {x}"
    )
    
    # Only update if selected page is different from current
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()
    
    # Show genetic status if available
    if 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None:
        st.sidebar.markdown("""
        <div class="genetics-active-badge">
            <div class="icon">🧬</div>
            <div class="title">Genetic Optimization Active</div>
            <div class="subtitle">Your plan includes genetic insights</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Genetic insights info card
        st.sidebar.markdown("""
        <div class="sidebar-section">
            <h3>Genetic Insights</h3>
        </div>
        <div class="sidebar-info-card">
            <h4>Personalized Based On Your Genes</h4>
            <p>Your nutrition plan is enhanced with insights from your genetic profile:</p>
            <ul>
                <li>Carbohydrate metabolism</li>
                <li>Fat sensitivity</li>
                <li>Nutrient processing</li>
                <li>Inflammation response</li>
                <li>Caffeine metabolism</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Add option to clear genetic data
        if st.sidebar.button("🗑️ Clear Genetic Data", type="secondary", key="clear_genetic_data_button"):
            # Clear all genetic-related data from the session
            if 'genetic_profile' in st.session_state:
                del st.session_state.genetic_profile
            
            if 'original_genetic_data' in st.session_state:
                del st.session_state.original_genetic_data
                
            if 'genetic_data_option' in st.session_state:
                st.session_state.genetic_data_option = "None"
                
            if 'show_genetic_insights' in st.session_state:
                del st.session_state.show_genetic_insights
            
            # Also clear any health assessment that might include genetic data
            if 'health_assessment' in st.session_state:
                del st.session_state.health_assessment
            
            st.sidebar.success("All genetic data has been cleared!")
            st.rerun()
    else:
        st.sidebar.markdown("""
        <div class="sidebar-section">
            <h3>About This App</h3>
        </div>
        <div class="sidebar-info-card">
            <h4>Personalized Nutrition Guidance</h4>
            <p>This application provides accessible, personalized nutrition guidance for individuals with diabetes, taking into account:</p>
            <ul>
                <li>Health metrics and diabetes status</li>
                <li>Socioeconomic context and resources</li>
                <li>Cultural food preferences</li>
                <li>Genetic profile (if provided)</li>
            </ul>
        </div>
        
        <div class="sidebar-info-card">
            <h4>Enhance Your Assessment</h4>
            <p>Upload genetic data on the Input Data page to receive more personalized recommendations tailored to your unique genetic profile.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <p>Developed by: Senthil Palanivelu</p>
        <p style="font-size: 12px; margin-top: 5px;">Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.page

def input_health_data():
    """
    Collect health-related data from the user and save to session state.
    
    Returns:
        dict: Dictionary containing user health information
    """
    # Initialize health_data in session state if it doesn't exist
    previous_health_data = st.session_state.health_data.copy() if 'health_data' in st.session_state else {}

    if 'health_data' not in st.session_state:
        st.session_state.health_data = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Use session state for each input to maintain values across reruns
        if 'age' not in st.session_state:
            st.session_state.age = 45  # Default value
        
        age = st.number_input(
            "Age", 
            min_value=18, 
            max_value=120, 
            value=st.session_state.age,
            key="age_input"
        )
        st.session_state.age = age
        
        if 'gender' not in st.session_state:
            st.session_state.gender = "Male"  # Default value
            
        gender = st.selectbox(
            "Gender", 
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(st.session_state.gender),
            key="gender_input"
        )
        st.session_state.gender = gender
        
        if 'weight' not in st.session_state:
            st.session_state.weight = 70.0  # Default value
            
        weight = st.number_input(
            "Weight (kg)", 
            min_value=30.0, 
            max_value=200.0, 
            value=st.session_state.weight, 
            step=0.1,
            key="weight_input"
        )
        st.session_state.weight = weight
        
        if 'height' not in st.session_state:
            st.session_state.height = 170.0  # Default value
            
        height = st.number_input(
            "Height (cm)", 
            min_value=100.0, 
            max_value=220.0, 
            value=st.session_state.height, 
            step=0.1,
            key="height_input"
        )
        st.session_state.height = height
        
        # Calculate BMI
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        st.metric("BMI", bmi, help="Body Mass Index")
        
        if 'activity_level' not in st.session_state:
            st.session_state.activity_level = "Moderately Active"  # Default value
            
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
            value=st.session_state.activity_level,
            key="activity_level_input"
        )
        st.session_state.activity_level = activity_level
    
    with col2:
        if 'diabetes_type' not in st.session_state:
            st.session_state.diabetes_type = "Type 2"  # Default value
            
        diabetes_type = st.selectbox(
            "Diabetes Type", 
            ["Type 1", "Type 2", "Gestational", "Prediabetes"],
            index=["Type 1", "Type 2", "Gestational", "Prediabetes"].index(st.session_state.diabetes_type),
            key="diabetes_type_input"
        )
        st.session_state.diabetes_type = diabetes_type
        
        if 'fasting_glucose' not in st.session_state:
            st.session_state.fasting_glucose = 120  # Default value
            
        fasting_glucose = st.number_input(
            "Fasting Blood Glucose (mg/dL)", 
            min_value=70, 
            max_value=300, 
            value=st.session_state.fasting_glucose,
            key="fasting_glucose_input"
        )
        st.session_state.fasting_glucose = fasting_glucose
        
        if 'postmeal_glucose' not in st.session_state:
            st.session_state.postmeal_glucose = 160  # Default value
            
        postmeal_glucose = st.number_input(
            "Post-meal Blood Glucose (mg/dL)", 
            min_value=70, 
            max_value=400, 
            value=st.session_state.postmeal_glucose,
            key="postmeal_glucose_input"
        )
        st.session_state.postmeal_glucose = postmeal_glucose
        
        if 'hba1c' not in st.session_state:
            st.session_state.hba1c = 7.0  # Default value
            
        hba1c = st.number_input(
            "HbA1c (%)", 
            min_value=4.0, 
            max_value=14.0, 
            value=st.session_state.hba1c, 
            step=0.1,
            key="hba1c_input"
        )
        st.session_state.hba1c = hba1c
        
        if 'dietary_restrictions' not in st.session_state:
            st.session_state.dietary_restrictions = []  # Default value
            
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Gluten-Free", "Lactose Intolerant", "Nut Allergies", "Shellfish Allergies"],
            default=st.session_state.dietary_restrictions,
            key="dietary_restrictions_input"
        )
        st.session_state.dietary_restrictions = dietary_restrictions
        
        if 'medications' not in st.session_state:
            st.session_state.medications = ""  # Default value
            
        medications = st.text_area(
            "Current Medications (one per line)",
            value=st.session_state.medications,
            key="medications_input"
        )
        st.session_state.medications = medications
        
        if 'other_conditions' not in st.session_state:
            st.session_state.other_conditions = ""  # Default value
            
        other_conditions = st.text_area(
            "Other Health Conditions (one per line)",
            value=st.session_state.other_conditions,
            key="other_conditions_input"
        )
        st.session_state.other_conditions = other_conditions

        if 'health_data' in st.session_state and previous_health_data != st.session_state.health_data:
            # Clear the last_assessed_data to indicate assessment is no longer current
            if 'last_assessed_data' in st.session_state:
                del st.session_state.last_assessed_data
    
    # Update the health_data dictionary with all values
    st.session_state.health_data = {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'bmi': bmi,
        'activity_level': activity_level,
        'diabetes_type': diabetes_type,
        'fasting_glucose': fasting_glucose,
        'postmeal_glucose': postmeal_glucose,
        'hba1c': hba1c,
        'dietary_restrictions': ", ".join(dietary_restrictions) if dietary_restrictions else "None",
        'medications': medications,
        'other_conditions': other_conditions
    }
    
    # Return the updated health data
    return st.session_state.health_data

def input_socioeconomic_data():
    """
    Collect socioeconomic data from the user and save to session state.
    
    Returns:
        dict: Dictionary containing user socioeconomic information
    """
    # Initialize socio_data in session state if it doesn't exist
    if 'socio_data' not in st.session_state:
        st.session_state.socio_data = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Location
        if 'location' not in st.session_state:
            st.session_state.location = ""
            
        location = st.text_input(
            "Location (Country/Region)",
            value=st.session_state.location,
            key="location_input"
        )
        st.session_state.location = location
        
        # Geographic Setting
        if 'geographic_setting' not in st.session_state:
            st.session_state.geographic_setting = "Urban"
            
        geographic_setting = st.selectbox(
            "Geographic Setting", 
            ["Urban", "Suburban", "Rural"],
            index=["Urban", "Suburban", "Rural"].index(st.session_state.geographic_setting 
                if 'geographic_setting' in st.session_state else "Urban"),
            key="geographic_setting_input"
        )
        st.session_state.geographic_setting = geographic_setting
        
        # Income Level
        if 'income_level' not in st.session_state:
            st.session_state.income_level = "Middle"
            
        income_level = st.selectbox(
            "Income Level",
            options=["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"],
            index=["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"].index(
                st.session_state.income_level if 'income_level' in st.session_state else "Middle"),
            key="income_level_input"
        )
        st.session_state.income_level = income_level
        
        # Education Level
        if 'education_level' not in st.session_state:
            st.session_state.education_level = "High School/Secondary"
            
        education_level = st.selectbox(
            "Education Level",
            ["Elementary/Primary", "High School/Secondary", "College/University", "Graduate/Professional"],
            index=["Elementary/Primary", "High School/Secondary", "College/University", "Graduate/Professional"].index(
                st.session_state.education_level if 'education_level' in st.session_state else "High School/Secondary"),
            key="education_level_input"
        )
        st.session_state.education_level = education_level
        
        # Literacy Level
        if 'literacy_level' not in st.session_state:
            st.session_state.literacy_level = "Moderate"
            
        literacy_level = st.selectbox(
            "Literacy Level",
            options=["Low", "Basic", "Moderate", "High"],
            index=["Low", "Basic", "Moderate", "High"].index(
                st.session_state.literacy_level if 'literacy_level' in st.session_state else "Moderate"),
            key="literacy_level_input"
        )
        st.session_state.literacy_level = literacy_level
    
    with col2:
        # Language Preferences
        if 'language_preferences' not in st.session_state:
            st.session_state.language_preferences = ""
            
        language_preferences = st.text_input(
            "Preferred Language(s)",
            value=st.session_state.language_preferences,
            key="language_preferences_input"
        )
        st.session_state.language_preferences = language_preferences
        
        # Technology Access
        if 'technology_access' not in st.session_state:
            st.session_state.technology_access = "Moderate"
            
        technology_access = st.selectbox(
            "Access to Technology",
            options=["Very Limited", "Limited", "Moderate", "Good", "Excellent"],
            index=["Very Limited", "Limited", "Moderate", "Good", "Excellent"].index(
                st.session_state.technology_access if 'technology_access' in st.session_state else "Moderate"),
            key="technology_access_input"
        )
        st.session_state.technology_access = technology_access
        
        # Healthcare Access
        if 'healthcare_access' not in st.session_state:
            st.session_state.healthcare_access = "Moderate"
            
        healthcare_access = st.selectbox(
            "Access to Healthcare",
            options=["Very Limited", "Limited", "Moderate", "Good", "Excellent"],
            index=["Very Limited", "Limited", "Moderate", "Good", "Excellent"].index(
                st.session_state.healthcare_access if 'healthcare_access' in st.session_state else "Moderate"),
            key="healthcare_access_input"
        )
        st.session_state.healthcare_access = healthcare_access
        
        # Local Food Availability
        if 'local_food_availability' not in st.session_state:
            st.session_state.local_food_availability = "Moderate"
            
        local_food_availability = st.selectbox(
            "Local Food Availability",
            ["Limited", "Moderate", "Abundant"],
            index=["Limited", "Moderate", "Abundant"].index(
                st.session_state.local_food_availability if 'local_food_availability' in st.session_state else "Moderate"),
            key="local_food_availability_input"
        )
        st.session_state.local_food_availability = local_food_availability
        
        # Grocery Budget
        if 'grocery_budget' not in st.session_state:
            st.session_state.grocery_budget = "Moderate"
            
        grocery_budget = st.selectbox(
            "Grocery Budget",
            options=["Very Limited", "Limited", "Moderate", "Comfortable", "Generous"],
            index=["Very Limited", "Limited", "Moderate", "Comfortable", "Generous"].index(
                st.session_state.grocery_budget if 'grocery_budget' in st.session_state else "Moderate"),
            key="grocery_budget_input"
        )
        st.session_state.grocery_budget = grocery_budget
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Cooking Facilities
        if 'cooking_facilities' not in st.session_state:
            st.session_state.cooking_facilities = []
            
        cooking_facilities = st.multiselect(
            "Cooking Facilities Available",
            ["Basic stove", "Oven", "Microwave", "Refrigerator", "Freezer", "Limited/Shared kitchen", "No cooking facilities"],
            default=st.session_state.cooking_facilities,
            key="cooking_facilities_input"
        )
        st.session_state.cooking_facilities = cooking_facilities
        
        # Meal Prep Time
        if 'meal_prep_time' not in st.session_state:
            st.session_state.meal_prep_time = "Limited"
            
        meal_prep_time = st.selectbox(
            "Time Available for Meal Preparation",
            options=["Very Limited", "Limited", "Moderate", "Substantial"],
            index=["Very Limited", "Limited", "Moderate", "Substantial"].index(
                st.session_state.meal_prep_time if 'meal_prep_time' in st.session_state else "Limited"),
            key="meal_prep_time_input"
        )
        st.session_state.meal_prep_time = meal_prep_time
    
    with col4:
        # Family Size
        if 'family_size' not in st.session_state:
            st.session_state.family_size = 1
            
        family_size = st.number_input(
            "Family Size (including yourself)", 
            min_value=1, 
            max_value=20, 
            value=st.session_state.family_size,
            key="family_size_input"
        )
        st.session_state.family_size = family_size
        
        # Support System
        if 'support_system' not in st.session_state:
            st.session_state.support_system = []
            
        support_system = st.multiselect(
            "Support System",
            ["Lives alone", "Family support", "Community support", "Healthcare support", "Limited support"],
            default=st.session_state.support_system,
            key="support_system_input"
        )
        st.session_state.support_system = support_system
        
        # Cultural Food Preferences
        if 'cultural_foods' not in st.session_state:
            st.session_state.cultural_foods = ""
            
        cultural_foods = st.text_area(
            "Cultural Food Preferences and Traditional Foods",
            value=st.session_state.cultural_foods,
            key="cultural_foods_input"
        )
        st.session_state.cultural_foods = cultural_foods
    
    # Update the socio_data dictionary with all values
    st.session_state.socio_data = {
        'location': location,
        'geographic_setting': geographic_setting,
        'income_level': income_level,
        'education_level': education_level,
        'literacy_level': literacy_level,
        'language_preferences': language_preferences,
        'technology_access': technology_access,
        'healthcare_access': healthcare_access,
        'local_food_availability': local_food_availability,
        'grocery_budget': grocery_budget,
        'cooking_facilities': ", ".join(cooking_facilities) if cooking_facilities else "Basic",
        'meal_prep_time': meal_prep_time,
        'family_size': family_size,
        'support_system': ", ".join(support_system) if support_system else "Limited",
        'cultural_foods': cultural_foods
    }
    
    return st.session_state.socio_data

def navigate_to_view_plan():
    """Function to navigate to view plan page."""
    st.session_state.page = "Nutrition Plan"