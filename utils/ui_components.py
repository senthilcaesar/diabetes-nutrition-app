"""
UI Components module for the Diabetes Nutrition Plan application.
Contains functions for creating and managing the user interface with a futuristic, sci-fi inspired design.
"""
import streamlit as st

def show_header():
    """
    Display the application header with a futuristic, sci-fi inspired design.
    """    
    # Check if genetic data is available to customize the header
    has_genetic_data = 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None
    
    # Hello
    # Add the particle animation background
    st.markdown('''
    <div class="neo-particles">
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
        <div class="neo-particle"></div>
    </div>
    ''', unsafe_allow_html=True)
    

def apply_custom_css():
    """
    Apply custom CSS styling to the application with a futuristic, sci-fi inspired design.
    """
    st.markdown("""
    <style>
        /* === GLOBAL STYLES === */
        /* Font styles and base elements */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');
        
        /* Force light mode by disabling color-scheme detection */
        :root {
            color-scheme: light only !important;
        }
        
        /* Force light mode for all elements */
        html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
            color-scheme: light only !important;
        }
        
        /* Force light mode for Streamlit elements */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarContent"], .main, .block-container, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
            color-scheme: light only !important;
        }
          

        /* === THEME COLORS === */
        /* Light mode theme variables */
        :root {
            /* Light theme color palette */
            --primary-color: #00003c;  /* Dark navy blue */
            --primary-light: #0000a0;  /* Lighter navy blue */
            --primary-dark: #000020;  /* Darker navy blue */
            --accent-color: #7B42F6;  /* Neon purple */
            --warning-color: #FFD600;  /* Neon yellow */
            --success-color: #00FF94;  /* Neon green */
            --info-color: #00003c;  /* Dark navy blue */
            --error-color: #FF3D71;  /* Neon red */
            
            /* Text colors */
            --text-color: #333333;  /* Dark gray for text */
            --text-muted: #666666;  /* Medium gray for muted text */
            --text-light: #999999;  /* Light gray for light text */
            
            /* Background colors */
            --bg-primary: #FFFFFF;  /* White background */
            --card-bg: #FFFFFF;  /* White card background */
            
            /* UI elements */
            --border-radius: 16px;
            --border-radius-lg: 24px;
            --border-radius-sm: 12px;
            --border-radius-full: 9999px;
            --border-angle: 10px;  /* For angled corners */
            
            /* Glows and shadows - lighter for light mode */
            --neon-glow-cyan: 0 0 5px rgba(0, 0, 60, 0.3), 0 0 10px rgba(0, 0, 60, 0.2);
            --neon-glow-magenta: 0 0 5px rgba(255, 0, 228, 0.3), 0 0 10px rgba(255, 0, 228, 0.2);
            --neon-glow-purple: 0 0 5px rgba(123, 66, 246, 0.3), 0 0 10px rgba(123, 66, 246, 0.2);
            --neon-glow-yellow: 0 0 5px rgba(255, 214, 0, 0.3), 0 0 10px rgba(255, 214, 0, 0.2);
            --neon-glow-green: 0 0 5px rgba(0, 255, 148, 0.3), 0 0 10px rgba(0, 255, 148, 0.2);
            
            --box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
            --box-shadow-md: 0 4px 15px -3px rgba(0, 0, 0, 0.07);
            --box-shadow-lg: 0 8px 25px -5px rgba(0, 0, 0, 0.08);
            
        /* Sidebar specific - darker text for better visibility */
        --sidebar-bg: #F0F0F0;
        --sidebar-element-bg: #FFFFFF;
        --sidebar-element-active-bg: linear-gradient(135deg, #64B5F6, #42A5F5);
        --sidebar-element-active-color: #FFFFFF;
        --sidebar-element-color: #333333;  /* Darker text */
        --sidebar-text-color: #333333;  /* Darker text */
        --sidebar-accent-color: #0066CC;  /* Darker blue */
        --sidebar-badge-bg: rgba(100, 181, 246, 0.1);
            
            /* Form elements */
            --input-bg: #FFFFFF;
            --input-border: #E0E0E0;
            --input-text: #333333;
            --input-focus-border: #64B5F6;
            --input-focus-shadow: rgba(100, 181, 246, 0.2);
            
            /* Transitions */
            --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Typography - Futuristic sci-fi fonts */
        body {
            font-family: 'Rajdhani', sans-serif;
            color: var(--text-color);
            line-height: 1.6;
            letter-spacing: 0.03em;
            background-color: var(--bg-primary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            margin-bottom: 1rem;
            letter-spacing: 0.05em;
            line-height: 1.2;
            text-transform: uppercase;
        }
        
        h1 {
            font-size: 2.5rem;
            color: var(--text-color);
            position: relative;
        }
        
        h2 {
            font-size: 2rem;
            color: var(--text-color);
            position: relative;
        }
        
        /* Remove the line below headers by default */
        h2::after {
            content: none !important;
            display: none !important;
        }
        
        /* Only show the line for specific headers where needed */
        .with-underline::after {
            content: "" !important;
            display: block !important;
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        h3 {
            font-size: 1.5rem;
            color: var(--text-color);
        }
        
        p {
            margin-bottom: 1.25rem;
            line-height: 1.7;
        }
        
        /* Monospace for data displays */
        .neo-data {
            font-family: 'Share Tech Mono', monospace;
            letter-spacing: 0.05em;
        }

        /* === LAYOUT & STRUCTURE === */
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none !important;}
        
        /* Force the entire app to take full height */
        .stApp {
            margin-top: -4rem !important;
            background-color: var(--bg-primary);
        }
        
        /* App container settings */
        .appview-container {
            padding-top: 0 !important;
        }
        
        /* Sidebar adjustments - futuristic dark panel */
        section[data-testid="stSidebar"] {
            top: 0 !important;
            padding-top: 1rem !important; /* Reduced padding to move content up */
            background: var(--bg-secondary);
            border-right: 1px solid #e0e0e0; /* Light shade of gray border */
            box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5);
        }
        
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ensure proper overflow handling */
        body {
            overflow-x: hidden;
        }
        
        /* Angled corner mixin (using pseudo-elements) */
        .neo-angled-corners {
            position: relative;
            clip-path: polygon(
                0 var(--border-angle), 
                var(--border-angle) 0, 
                100% 0, 
                100% calc(100% - var(--border-angle)), 
                calc(100% - var(--border-angle)) 100%, 
                0 100%
            );
        }
        

                
        /* Particle animation background */
        .neo-particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }
        
        .neo-particle {
            position: absolute;
            width: 2px;
            height: 2px;
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
        }
        
        .neo-particle:nth-child(1) { top: 10%; left: 20%; }
        .neo-particle:nth-child(2) { top: 40%; left: 50%; }
        .neo-particle:nth-child(3) { top: 70%; left: 30%; }
        .neo-particle:nth-child(4) { top: 20%; left: 80%; }
        .neo-particle:nth-child(5) { top: 60%; left: 10%; }
        .neo-particle:nth-child(6) { top: 30%; left: 60%; }
        .neo-particle:nth-child(7) { top: 80%; left: 70%; }
        .neo-particle:nth-child(8) { top: 50%; left: 40%; }
        .neo-particle:nth-child(9) { top: 15%; left: 90%; }
        .neo-particle:nth-child(10) { top: 85%; left: 25%; }
        .neo-particle:nth-child(11) { top: 45%; left: 75%; }
        .neo-particle:nth-child(12) { top: 75%; left: 55%; }
        
        @keyframes float {
            0% {
                transform: translateY(0) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(100px);
                opacity: 0;
            }
        }
        
        .neo-header-content {
            display: flex;
            align-items: center;
            position: relative;
            z-index: 1;
            margin: 0;
            padding: 0;
        }
        
        .neo-header-icon {
            flex: 0 0 150px;
            margin-right: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .neo-header-text {
            flex: 1;
        }
        
        .neo-title-container {
            position: relative;
            margin: 0 0 0.5rem 0;
            padding: 0;
        }
        
        .neo-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0 0 0.25rem 0;
            padding: 0;
            letter-spacing: 0.1em;
            color: var(--text-color);
            text-shadow: 0 0 10px rgba(0, 0, 60, 0.5);
            line-height: 1.1;
        }
        
        .neo-title-prefix {
            color: var(--primary-color);
            font-weight: 400;
            margin-right: 0.5rem;
        }
        
        .neo-subtitle {
            font-family: 'Share Tech Mono', monospace;
            color: var(--text-muted);
            font-size: 1rem;
            letter-spacing: 0.2em;
            margin-bottom: 1.5rem;
        }
        
        .neo-highlight {
            color: var(--primary-color);
            font-weight: 700;
        }
        
        /* Futuristic DNA Animation */
        .neo-dna-animation {
            width: 120px;
            height: 120px;
            position: relative;
            perspective: 1000px;
        }
        
        .neo-dna-ring {
            position: absolute;
            border: 2px solid transparent;
            border-radius: 50%;
            width: 100%;
            height: 100%;
            box-shadow: var(--neon-glow-cyan);
        }
        
        .neo-dna-ring:nth-child(1) {
            border-top: 2px solid var(--primary-color);
            border-bottom: 2px solid var(--primary-color);
        }
        
        .neo-dna-ring:nth-child(2) {
            border-left: 2px solid var(--secondary-color);
            border-right: 2px solid var(--secondary-color);
        }
        
        .neo-dna-ring:nth-child(3) {
            border-top: 2px solid var(--accent-color);
            border-bottom: 2px solid var(--accent-color);
            width: 80%;
            height: 80%;
            top: 10%;
            left: 10%;
        }
        
        /* Futuristic Pulse Animation with hexagons */
        .neo-pulse-animation {
            width: 120px;
            height: 120px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .neo-hexagon {
            position: absolute;
            width: 60px;
            height: 60px;
            background-color: transparent;
            opacity: 1;
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            border: 2px solid var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .neo-hexagon:nth-child(1) {
            /* No animation delay */
        }
        
        .neo-hexagon:nth-child(2) {
            border-color: var(--secondary-color);
            box-shadow: var(--neon-glow-magenta);
        }
        
        .neo-hexagon:nth-child(3) {
            border-color: var(--accent-color);
            box-shadow: var(--neon-glow-purple);
        }
        
        
        /* Futuristic badges */
        .neo-badge, .neo-upgrade-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
            border-radius: var(--border-radius-sm);
        }
        
        .neo-badge {
            background-color: rgba(0, 0, 60, 0.1);
            color: var(--primary-color);
            border: 1px solid var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .neo-upgrade-badge {
            background-color: rgba(255, 0, 228, 0.1);
            color: var(--secondary-color);
            border: 1px solid var(--secondary-color);
            box-shadow: var(--neon-glow-magenta);
        }
        
        .neo-badge-glow {
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 100%;
            background: none;
        }
        
        @keyframes neo-badge-glow {
            0% { left: -100%; }
            100% { left: 200%; }
        }
        
        .neo-badge-icon, .neo-badge-text {
            position: relative;
            z-index: 1;
        }
        
        .neo-badge-icon {
            margin-right: 0.75rem;
            font-size: 1rem;
        }
        
        /* === TABS & NAVIGATION === */
        /* Futuristic tab styling - similar to sidebar radio buttons */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            border-bottom: none;
            padding-bottom: 0;
            background: transparent;
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
        }
        
  
        
        .stTabs [data-baseweb="tab"] {
            padding: 16px 30px 16px 16px !important; /* Consistent padding for all tabs */
            margin: 5px 0 !important;
            border-radius: var(--border-radius) !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            background-color: #FFFFFF !important; /* White background */
            color: #000000 !important; /* Dark black text for better visibility */
            border: 1px solid rgba(0, 0, 60, 0.2) !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-weight: 700 !important; /* Bolder text for better visibility */
            box-shadow: var(--box-shadow) !important;
            position: relative;
            overflow: hidden;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            font-size: 0.9rem !important;
            min-width: 200px;
            text-align: center;
            width: auto !important; /* Prevent width changes */
            box-sizing: border-box !important; /* Include padding in width calculation */
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(229, 228, 226, 0.0); /* Light sky blue background */
            z-index: 0;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        
        .stTabs [data-baseweb="tab"]:hover::before {
            opacity: 1;
        }
        
        /* Only apply hover effects to non-selected tabs */
        .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
            background-color: #E5E4E2 !important; /* Very light gray background on hover */
            border: 1px solid var(--primary-color) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #87CEEB !important; /* Sky blue for selected tab */
            color: var(--primary-color) !important;
            font-weight: 700 !important;
            box-shadow: var(--neon-glow-cyan) !important;
            border: 1px solid var(--primary-color) !important;
        }
        
        /* Completely remove any red line or indicator from selected tabs */
        .stTabs [data-baseweb="tab"][aria-selected="true"]::after,
        .stTabs [data-baseweb="tab"][aria-selected="true"]::before,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]::after,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]::before {
            display: none !important;
            content: none !important;
            border: none !important;
            background: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        
   
        
        /* Remove any hover effects that might show red lines */
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]:hover::after,
        .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"]:hover::before {
            display: none !important;
            content: none !important;
            border: none !important;
            background: none !important;
        }
        
        /* Remove any indicator or highlight elements */
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"],
        .stTabs [role="tablist"] [data-baseweb="tab-highlight"],
        .stTabs [role="tablist"] [data-baseweb="tab-border"] {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            border: none !important;
            background: none !important;
        }
        
        .stTabs [aria-selected="true"]::after {
            content: "▶";
            position: absolute;
            top: 50%;
            right: 12px;
            transform: translateY(-50%);
            color: var(--primary-color);
            font-size: 0.75rem;
            text-shadow: var(--neon-glow-cyan);
        }
        
        /* Fix spacing around tab panels */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1.5rem !important;
            background: #f5f5f5; /* Light shade of gray */
            border-radius: var(--border-radius-lg);
            border: 1px solid #e0e0e0; /* Light shade of gray border */
            padding: 1.5rem !important;
            margin-top: 0.8rem; /* Increased space between tabs and panel */
            box-shadow: var(--box-shadow);
            color: #000000 !important; /* Force black text in tab panels */
        }
        
        /* Force all text in tab panels to be black - with !important and higher specificity */
.stTabs [data-baseweb="tab-panel"] p,
.stTabs [data-baseweb="tab-panel"] span,
.stTabs [data-baseweb="tab-panel"] div,
.stTabs [data-baseweb="tab-panel"] h1,
.stTabs [data-baseweb="tab-panel"] h2,
.stTabs [data-baseweb="tab-panel"] h3,
.stTabs [data-baseweb="tab-panel"] h4,
.stTabs [data-baseweb="tab-panel"] h5,
.stTabs [data-baseweb="tab-panel"] h6,
.stTabs [data-baseweb="tab-panel"] li,
.stTabs [data-baseweb="tab-panel"] a,
.stTabs [data-baseweb="tab-panel"] label,
.stTabs [data-baseweb="tab-panel"] button,
/* Target more specific elements */
.stTabs [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"],
.stTabs [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] p,
.stTabs [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] span,
.stTabs [data-baseweb="tab-panel"] [data-testid="stMarkdownContainer"] div,
.stTabs [data-baseweb="tab-panel"] [data-testid="stText"],
.stTabs [data-baseweb="tab-panel"] [data-testid="stText"] p,
.stTabs [data-baseweb="tab-panel"] [data-testid="stText"] span,
.stTabs [data-baseweb="tab-panel"] [data-testid="stText"] div {
    color: #000000 !important;
    opacity: 1 !important;
    font-weight: normal !important;
}
        
        /* Target the specific light blue panel in the genetic data tab */
        .stTabs [data-baseweb="tab-panel"] > div {
            color: #000000 !important;
        }
        
        /* Target any alert or info boxes */
        .stTabs [data-baseweb="tab-panel"] .stAlert,
        .stTabs [data-baseweb="tab-panel"] .stInfo,
        .stTabs [data-baseweb="tab-panel"] .stSuccess,
        .stTabs [data-baseweb="tab-panel"] .stWarning,
        .stTabs [data-baseweb="tab-panel"] .stError {
            color: #000000 !important;
        }
        
        /* Target any markdown or text within the light blue panel */
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: rgb(240, 242, 246)"] *,
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: #f0f2f6"] *,
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: rgb(241, 246, 253)"] *,
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: #f1f6fd"] *,
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: rgb(135, 206, 235)"] *,
        .stTabs [data-baseweb="tab-panel"] [style*="background-color: #87CEEB"] * {
            color: #000000 !important;
            opacity: 1 !important;
            font-weight: normal !important;
        }
        
        /* Force all text in the genetic data tab to be black */
        .stTabs [data-baseweb="tab-panel"] .element-container,
        .stTabs [data-baseweb="tab-panel"] .element-container *,
        .stTabs [data-baseweb="tab-panel"] .stMarkdown,
        .stTabs [data-baseweb="tab-panel"] .stMarkdown *,
        .stTabs [data-baseweb="tab-panel"] p,
        .stTabs [data-baseweb="tab-panel"] h1,
        .stTabs [data-baseweb="tab-panel"] h2,
        .stTabs [data-baseweb="tab-panel"] h3 {
            color: #000000 !important;
            opacity: 1 !important;
        }
        
        /* Target the specific light blue info box in the genetic data tab */
        .stTabs [data-baseweb="tab-panel"] .stAlert,
        .stTabs [data-baseweb="tab-panel"] .stInfo,
        .stTabs [data-baseweb="tab-panel"] .stInfo *,
        .stTabs [data-baseweb="tab-panel"] .stAlert *,
        .stTabs [data-baseweb="tab-panel"] [data-testid="stCaptionContainer"],
        .stTabs [data-baseweb="tab-panel"] [data-testid="stCaptionContainer"] * {
            color: #000000 !important;
            opacity: 1 !important;
            font-weight: normal !important;
        }
        
        .stTabs [data-baseweb="tab-content"] {
            padding: 0px !important;
        }
        
        /* === CARDS & CONTAINERS === */
        /* Futuristic card styling */
        .card-container {
            background-color: #FFFFFF;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid #e0e0e0;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .card-container:hover {
            box-shadow: var(--neon-glow-cyan);
            border-color: var(--primary-color);
        }
        
        .card-container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        /* Futuristic plan header */
        .plan-header {
            background-color: #f5f5f5;
            padding: 2.5rem;
            border-radius: var(--border-radius-lg);
            color: var(--text-color);
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: var(--box-shadow);
            position: relative;
            overflow: hidden;
            border: 1px solid #e0e0e0;
        }
        
        .plan-header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 0;
            background: none;
            z-index: 0;
        }
        
        .plan-header h2 {
            position: relative;
            z-index: 1;
            color: #333333;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }
        
        .plan-header p {
            position: relative;
            z-index: 1;
            opacity: 0.9;
            font-size: 1.125rem;
        }
        
        /* Futuristic plan sections */
        .plan-section {
            background-color: #FFFFFF;
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            margin-bottom: 2rem;
            border: 1px solid #e0e0e0;
            position: relative;
            overflow: hidden;
        }
        
        .plan-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 3px;
            background: var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .plan-section h3 {
            color: var(--primary-dark);
            border-bottom: 2px solid rgba(226, 232, 240, 0.8);
            padding-bottom: 0.75rem;
            margin-bottom: 1.25rem;
            font-weight: 600;
        }
        
        /* Meal cards */
        .meal-card {
            border: 1px solid #e0e0e0;
            border-radius: var(--border-radius);
            padding: 1.25rem;
            margin-bottom: 1rem;
            background-color: #FFFFFF;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .meal-card:hover {
            box-shadow: var(--box-shadow-md);
            transform: translateY(-3px);
        }
        
        .meal-card::after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-light), var(--secondary-light));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }
        
        .meal-card:hover::after {
            transform: scaleX(1);
        }
        
        .meal-title {
            font-weight: 600;
            color: var(--primary-dark);
            margin-bottom: 0.75rem;
            font-size: 1.125rem;
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            padding-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }
        
        .meal-title::before {
            content: "•";
            color: var(--primary-color);
            font-size: 1.5rem;
            margin-right: 0.5rem;
            line-height: 0;
        }
        
        /* Foods limit section */
        .limit-section {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(251, 191, 36, 0.1));
            border: 1px solid rgba(245, 158, 11, 0.2);
            padding: 1.25rem;
            border-radius: var(--border-radius);
            margin: 1.25rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .limit-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: var(--warning-color);
            border-radius: 5px;
        }
        
        .limit-section h2 {
            color: var(--warning-color);
            font-weight: 600;
            margin-bottom: 0.75rem;
            font-size: 1.25rem;
        }
        
        /* === HEALTH ASSESSMENT STYLING === */
        /* Assessment sections */
        .health-assessment-section {
            margin-bottom: 1.75rem;
            padding: 1.75rem;
            background-color: #FFFFFF;
            border-radius: var(--border-radius-lg);
            box-shadow: var(--box-shadow);
            border: 1px solid #e0e0e0;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .health-assessment-section:hover {
            box-shadow: var(--box-shadow-md);
            transform: translateY(-3px);
        }
        
        .health-assessment-section h2 {
            font-size: 1.5rem;
            color: var(--primary-dark);
            margin-top: 0;
            margin-bottom: 1rem;
            border-bottom: 2px solid rgba(226, 232, 240, 0.8);
            padding-bottom: 0.75rem;
            font-weight: 600;
        }
        
        .health-assessment-section h3 {
            font-size: 1.25rem;
            color: var(--primary-color);
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
        }
        
        /* Color-coded assessment sections with modern gradients */
        .summary-section {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(79, 70, 229, 0.1) 100%);
            position: relative;
        }
        
        .summary-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--primary-color), var(--primary-dark));
            border-radius: 5px;
        }
        
        .diabetes-management-section {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(37, 99, 235, 0.1) 100%);
            position: relative;
        }
        
        .diabetes-management-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--info-color), #2563eb);
            border-radius: 5px;
        }
        
        .risks-section {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(220, 38, 38, 0.1) 100%);
            position: relative;
        }
        
        .risks-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--error-color), #dc2626);
            border-radius: 5px;
        }
        
        .care-plans-section {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.1) 100%);
            position: relative;
        }
        
        .care-plans-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--secondary-color), var(--secondary-dark));
            border-radius: 5px;
        }
        
        .concerns-section {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(217, 119, 6, 0.1) 100%);
            position: relative;
        }
        
        .concerns-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--warning-color), #d97706);
            border-radius: 5px;
        }
        
        .recommendations-section {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.1) 100%);
            position: relative;
        }
        
        .recommendations-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, var(--secondary-color), var(--secondary-dark));
            border-radius: 5px;
        }
        
        .genetic-section {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.05) 0%, rgba(109, 40, 217, 0.1) 100%);
            position: relative;
        }
        
        .genetic-section::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            background: linear-gradient(to bottom, #7c3aed, #6d28d9);
            border-radius: 5px;
        }
        
        /* === BUTTONS & INTERACTIVE ELEMENTS === */
        /* Futuristic button styling */
        .stButton button {
            border-radius: var(--border-radius) !important;
            padding: 0.75rem 2rem !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-weight: 500 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            transition: var(--transition) !important;
            box-shadow: var(--box-shadow) !important;
            position: relative !important;
            overflow: hidden !important;
            font-size: 0.85rem !important;
        }
        
        .stButton button::before {
            content: "" !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 0 !important;
            height: 100% !important;
            background: none !important;
        }
        
        @keyframes neo-button-glow {
            0% { left: -100%; }
            100% { left: 200%; }
        }
        
                .stButton button[kind="primary"] {
            background-color: white !important; /* White background by default */
            border: 1px solid var(--primary-color) !important;
            color: var(--primary-color) !important;
        }

        
        /* Primary button - neon cyan */
        .stButton button[kind="secondary"] {
            background-color: white !important; /* White background by default */
            border: 1px solid var(--primary-color) !important;
            color: var(--primary-color) !important;
        }

  
        
        /* Success message - lighter, airier */
        .success-message {
            padding: 1.5rem;
            border-radius: var(--border-radius-lg);
            animation: fadeIn 0.5s ease-in-out;
            background: linear-gradient(135deg, rgba(165, 214, 167, 0.1), rgba(129, 199, 132, 0.15));
            border: 1px solid rgba(165, 214, 167, 0.25);
            position: relative;
            overflow: hidden;
            box-shadow: var(--box-shadow);
        }
        
        .success-message::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(to bottom, var(--secondary-light), var(--secondary-color));
            opacity: 0.8;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Error message - lighter, airier */
        .error-message {
            padding: 1.5rem;
            border-radius: var(--border-radius-lg);
            animation: fadeIn 0.5s ease-in-out;
            background: linear-gradient(135deg, rgba(229, 115, 115, 0.1), rgba(239, 154, 154, 0.15));
            border: 1px solid rgba(229, 115, 115, 0.25);
            position: relative;
            overflow: hidden;
            box-shadow: var(--box-shadow);
        }
        
        .error-message::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(to bottom, var(--error-color), #EF5350);
            opacity: 0.8;
        }
        
        /* === DATA INPUT ELEMENTS === */
        /* Make all input field labels bold with stronger selectors */
        div[data-testid="stForm"] label,
        div.stNumberInput label,
        div.stTextInput label,
        div.stSelectbox label,
        div.stMultiSelect label,
        div.stTextArea label,
        div.stDateInput label,
        div.stTimeInput label,
        div.stSlider label,
        div.stFileUploader label,
        div[data-baseweb="form-control"] label,
        div[data-testid="stVerticalBlock"] label {
            font-weight: 900 !important;
            font-family: 'Orbitron', sans-serif !important;
            color: #000000 !important;
            font-size: 1rem !important;
            letter-spacing: 0.05em !important;
        }
        
        /* Futuristic input fields with stronger selectors */
        .stTextInput > div > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"] {
            border-radius: var(--border-radius) !important;
            border: none !important;
            border-color: transparent !important;
            background-color: white !important;
            transition: var(--transition) !important;
            font-family: 'Share Tech Mono', monospace !important;
            box-shadow: none !important;
        }
        
        .stTextInput > div > div:focus-within,
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="base-input"]:focus-within {
            border: none !important;
            border-color: transparent !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Futuristic select boxes with stronger selectors */
        .stSelectbox > div > div > div,
        div[data-baseweb="select"] > div,
        div[role="combobox"] {
            border-radius: var(--border-radius) !important;
            border: none !important;
            border-color: transparent !important;
            background-color: white !important;
            transition: var(--transition) !important;
            font-family: 'Share Tech Mono', monospace !important;
            box-shadow: none !important;
            caret-color: transparent !important; /* Hide the blinking cursor */
        }
        
        .stSelectbox > div > div > div:focus-within,
        div[data-baseweb="select"] > div:focus-within,
        div[role="combobox"]:focus-within {
            border: none !important;
            border-color: transparent !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Futuristic number inputs with stronger selectors */
        .stNumberInput > div > div,
        input[type="number"] {
            border-radius: var(--border-radius) !important;
            border: none !important;
            border-color: transparent !important;
            background-color: white !important;
            transition: var(--transition) !important;
            font-family: 'Share Tech Mono', monospace !important;
            box-shadow: none !important;
        }
        
        .stNumberInput > div > div:focus-within,
        input[type="number"]:focus-within {
            border: none !important;
            border-color: transparent !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Extremely aggressive approach to hide increment/decrement buttons */
        .stNumberInput button,
        .stNumberInput [role="button"],
        .stNumberInput [data-testid*="Increment"],
        .stNumberInput [data-testid*="Decrement"],
        .stNumberInput button[aria-label*="Increment"],
        .stNumberInput button[aria-label*="Decrement"],
        .stNumberInput div > button,
        .stNumberInput > div > div > button,
        .stNumberInput > div > div > div > button,
        .stNumberInput button:first-child,
        .stNumberInput button:last-child,
        .stNumberInput button:nth-child(1),
        .stNumberInput button:nth-child(2),
        .stNumberInput button:nth-child(3),
        .stNumberInput button:nth-child(n),
        div[data-testid*="stNumberInput"] button,
        div[data-baseweb*="input-container"] button,
        div[data-baseweb*="numberinput"] button {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            position: absolute !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            clip-path: inset(50%) !important;
        }
        
        /* Force number input to take full width without buttons */
        .stNumberInput input[type="number"],
        div[data-testid*="stNumberInput"] input[type="number"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            padding-right: 8px !important;
            padding-left: 8px !important;
            box-sizing: border-box !important;
        }
        
        /* Remove spinner buttons from number inputs for all browsers */
        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {
            -webkit-appearance: none !important;
            appearance: none !important;
            margin: 0 !important;
            display: none !important;
        }
        
        input[type="number"] {
            -moz-appearance: textfield !important;
            appearance: textfield !important;
        }
        
        /* Futuristic text areas with stronger selectors */
        .stTextArea > div > div,
        textarea {
            border-radius: var(--border-radius) !important;
            border: none !important;
            border-color: transparent !important;
            background-color: white !important;
            transition: var(--transition) !important;
            font-family: 'Share Tech Mono', monospace !important;
            box-shadow: none !important;
        }
        
        .stTextArea > div > div:focus-within,
        textarea:focus-within {
            border: none !important;
            border-color: transparent !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
/* Futuristic multiselect with stronger selectors */
.stMultiSelect > div > div > div,
div[role="listbox"] {
    border-radius: var(--border-radius) !important;
    border: 1px solid #e0e0e0 !important; /* Light border for better visibility */
    background-color: white !important;
    transition: var(--transition) !important;
    font-family: 'Share Tech Mono', monospace !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important; /* Subtle shadow for depth */
    caret-color: transparent !important; /* Hide the blinking cursor */
}

.stMultiSelect > div > div > div:hover {
    border-color: #b0b0b0 !important; /* Darker border on hover */
}

.stMultiSelect > div > div > div:focus-within,
div[role="listbox"]:focus-within {
    border: 1px solid var(--primary-color) !important;
    box-shadow: var(--neon-glow-cyan) !important;
}

/* Improve multiselect dropdown styling */
div[role="listbox"] {
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
    z-index: 1000 !important; /* Ensure dropdown appears above other elements */
}


/* Style for selected items in multiselect */
[data-baseweb="tag"] {
    background-color: #f0f0f0 !important;
    border: 1px solid #d0d0d0 !important;
    margin: 2px !important;
    padding: 4px 8px !important;
}

[data-baseweb="tag"]:hover {
    background-color: #e0e0e0 !important;
}
        
        /* Force remove all borders from input elements */
        input, select, textarea, button {
            border: none !important;
            border-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* Extremely aggressive approach to remove all borders */
        /* Target all possible input elements and their containers */
        input, 
        select, 
        textarea, 
        button,
        [data-baseweb*="input"],
        [data-baseweb*="select"],
        [data-baseweb*="textarea"],
        [data-baseweb*="phone-input"],
        [data-baseweb*="input-container"],
        [data-baseweb*="form-control"],
        [data-baseweb*="popover"],
        [data-baseweb*="menu"],
        [data-baseweb*="list"],
        [data-baseweb*="select-dropdown"],
        [data-testid*="stForm"],
        .stNumberInput,
        .stTextInput,
        .stSelectbox,
        .stTextArea,
        .stMultiSelect,
        .stDateInput,
        .stTimeInput,
        .stFileUploader,
        div[role="combobox"],
        div[role="listbox"],
        div[role="textbox"],
        div[role="spinbutton"],
        div[class*="input"],
        div[class*="select"],
        div[class*="text"],
        div[class*="field"],
        div[class*="control"],
        div[class*="form"],
        div[class*="Input"],
        div[class*="Select"],
        div[class*="Text"],
        div[class*="Field"],
        div[class*="Control"],
        div[class*="Form"],
        /* Target all children of these elements */
        [data-baseweb*="input"] *,
        [data-baseweb*="select"] *,
        [data-baseweb*="textarea"] *,
        [data-baseweb*="phone-input"] *,
        [data-baseweb*="input-container"] *,
        [data-baseweb*="form-control"] *,
        [data-baseweb*="popover"] *,
        [data-baseweb*="menu"] *,
        [data-baseweb*="list"] *,
        [data-baseweb*="select-dropdown"] *,
        [data-testid*="stForm"] *,
        .stNumberInput *,
        .stTextInput *,
        .stSelectbox *,
        .stTextArea *,
        .stMultiSelect *,
        .stDateInput *,
        .stTimeInput *,
        .stFileUploader *,
        div[role="combobox"] *,
        div[role="listbox"] *,
        div[role="textbox"] *,
        div[role="spinbutton"] *,
        div[class*="input"] *,
        div[class*="select"] *,
        div[class*="text"] *,
        div[class*="field"] *,
        div[class*="control"] *,
        div[class*="form"] *,
        div[class*="Input"] *,
        div[class*="Select"] *,
        div[class*="Text"] *,
        div[class*="Field"] *,
        div[class*="Control"] *,
        div[class*="Form"] * {
            border: none !important;
            border-color: transparent !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* Target all states: focus, hover, active, focus-within, etc. */
        input:focus, 
        select:focus, 
        textarea:focus, 
        button:focus,
        input:hover, 
        select:hover, 
        textarea:hover, 
        button:hover,
        input:active, 
        select:active, 
        textarea:active, 
        button:active,
        [data-baseweb*="input"]:focus,
        [data-baseweb*="select"]:focus,
        [data-baseweb*="textarea"]:focus,
        [data-baseweb*="phone-input"]:focus,
        [data-baseweb*="input-container"]:focus,
        [data-baseweb*="form-control"]:focus,
        [data-baseweb*="popover"]:focus,
        [data-baseweb*="menu"]:focus,
        [data-baseweb*="list"]:focus,
        [data-baseweb*="select-dropdown"]:focus,
        [data-baseweb*="input"]:hover,
        [data-baseweb*="select"]:hover,
        [data-baseweb*="textarea"]:hover,
        [data-baseweb*="phone-input"]:hover,
        [data-baseweb*="input-container"]:hover,
        [data-baseweb*="form-control"]:hover,
        [data-baseweb*="popover"]:hover,
        [data-baseweb*="menu"]:hover,
        [data-baseweb*="list"]:hover,
        [data-baseweb*="select-dropdown"]:hover,
        [data-baseweb*="input"]:active,
        [data-baseweb*="select"]:active,
        [data-baseweb*="textarea"]:active,
        [data-baseweb*="phone-input"]:active,
        [data-baseweb*="input-container"]:active,
        [data-baseweb*="form-control"]:active,
        [data-baseweb*="popover"]:active,
        [data-baseweb*="menu"]:active,
        [data-baseweb*="list"]:active,
        [data-baseweb*="select-dropdown"]:active,
        [data-baseweb*="input"]:focus-within,
        [data-baseweb*="select"]:focus-within,
        [data-baseweb*="textarea"]:focus-within,
        [data-baseweb*="phone-input"]:focus-within,
        [data-baseweb*="input-container"]:focus-within,
        [data-baseweb*="form-control"]:focus-within,
        [data-baseweb*="popover"]:focus-within,
        [data-baseweb*="menu"]:focus-within,
        [data-baseweb*="list"]:focus-within,
        [data-baseweb*="select-dropdown"]:focus-within,
        [data-testid*="stForm"]:focus,
        [data-testid*="stForm"]:hover,
        [data-testid*="stForm"]:active,
        [data-testid*="stForm"]:focus-within,
        .stNumberInput:focus,
        .stTextInput:focus,
        .stSelectbox:focus,
        .stTextArea:focus,
        .stMultiSelect:focus,
        .stDateInput:focus,
        .stTimeInput:focus,
        .stFileUploader:focus,
        .stNumberInput:hover,
        .stTextInput:hover,
        .stSelectbox:hover,
        .stTextArea:hover,
        .stMultiSelect:hover,
        .stDateInput:hover,
        .stTimeInput:hover,
        .stFileUploader:hover,
        .stNumberInput:active,
        .stTextInput:active,
        .stSelectbox:active,
        .stTextArea:active,
        .stMultiSelect:active,
        .stDateInput:active,
        .stTimeInput:active,
        .stFileUploader:active,
        .stNumberInput:focus-within,
        .stTextInput:focus-within,
        .stSelectbox:focus-within,
        .stTextArea:focus-within,
        .stMultiSelect:focus-within,
        .stDateInput:focus-within,
        .stTimeInput:focus-within,
        .stFileUploader:focus-within,
        div[role="combobox"]:focus,
        div[role="listbox"]:focus,
        div[role="textbox"]:focus,
        div[role="spinbutton"]:focus,
        div[role="combobox"]:hover,
        div[role="listbox"]:hover,
        div[role="textbox"]:hover,
        div[role="spinbutton"]:hover,
        div[role="combobox"]:active,
        div[role="listbox"]:active,
        div[role="textbox"]:active,
        div[role="spinbutton"]:active,
        div[role="combobox"]:focus-within,
        div[role="listbox"]:focus-within,
        div[role="textbox"]:focus-within,
        div[role="spinbutton"]:focus-within,
        div[class*="input"]:focus,
        div[class*="select"]:focus,
        div[class*="text"]:focus,
        div[class*="field"]:focus,
        div[class*="control"]:focus,
        div[class*="form"]:focus,
        div[class*="Input"]:focus,
        div[class*="Select"]:focus,
        div[class*="Text"]:focus,
        div[class*="Field"]:focus,
        div[class*="Control"]:focus,
        div[class*="Form"]:focus,
        div[class*="input"]:hover,
        div[class*="select"]:hover,
        div[class*="text"]:hover,
        div[class*="field"]:hover,
        div[class*="control"]:hover,
        div[class*="form"]:hover,
        div[class*="Input"]:hover,
        div[class*="Select"]:hover,
        div[class*="Text"]:hover,
        div[class*="Field"]:hover,
        div[class*="Control"]:hover,
        div[class*="Form"]:hover,
        div[class*="input"]:active,
        div[class*="select"]:active,
        div[class*="text"]:active,
        div[class*="field"]:active,
        div[class*="control"]:active,
        div[class*="form"]:active,
        div[class*="Input"]:active,
        div[class*="Select"]:active,
        div[class*="Text"]:active,
        div[class*="Field"]:active,
        div[class*="Control"]:active,
        div[class*="Form"]:active,
        div[class*="input"]:focus-within,
        div[class*="select"]:focus-within,
        div[class*="text"]:focus-within,
        div[class*="field"]:focus-within,
        div[class*="control"]:focus-within,
        div[class*="form"]:focus-within,
        div[class*="Input"]:focus-within,
        div[class*="Select"]:focus-within,
        div[class*="Text"]:focus-within,
        div[class*="Field"]:focus-within,
        div[class*="Control"]:focus-within,
        div[class*="Form"]:focus-within {
            border: none !important;
            border-color: transparent !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* Target all validation states */
        [aria-invalid="true"],
        [aria-invalid="true"] *,
        [data-invalid="true"],
        [data-invalid="true"] *,
        .invalid,
        .invalid *,
        .error,
        .error *,
        .has-error,
        .has-error * {
            border: none !important;
            border-color: transparent !important;
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* Override Streamlit's default accent colors for futuristic form elements */
        [data-baseweb="select"] [data-baseweb="tag"] {
            background-color: rgba(0, 240, 255, 0.2) !important;
            border: 1px solid var(--primary-color) !important;
            border-radius: var(--border-radius-sm) !important;
            color: var(--primary-color) !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        
        [data-baseweb="base-input"] {
            border-color: var(--primary-color) !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        
        /* Futuristic radio buttons */
        [data-baseweb="radio"] [data-checked="true"] {
            color: var(--primary-color) !important;
        }
        
        /* Futuristic checkboxes */
        [data-baseweb="checkbox"] [data-checked="true"] {
            background-color: var(--primary-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Futuristic slider */
        [data-testid="stSlider"] > div > div > div {
            background-color: var(--primary-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Futuristic slider thumb */
        [data-testid="stSlider"] > div > div > div > div {
            background-color: var(--bg-primary) !important;
            border: 2px solid var(--primary-color) !important;
            box-shadow: var(--neon-glow-cyan) !important;
            transition: var(--transition) !important;
        }
        
        [data-testid="stSlider"] > div > div > div > div:hover {
            transform: scale(1.2) !important;
            box-shadow: var(--neon-glow-cyan) !important;
        }
        
        /* Metrics styling */
        [data-testid="stMetric"] {
            background-color: white !important;
            border: 1px solid #e0e0e0 !important; /* Light shade of gray border */
            border-radius: 4px !important;
            padding: 1rem !important;
            box-shadow: none !important;
            transition: none !important;
        }
        
        [data-testid="stMetric"]:hover {
            border-color: #e0e0e0 !important;
            box-shadow: none !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif !important;
            color: #333333 !important;
            font-size: 0.85rem !important;
            letter-spacing: normal !important;
            text-transform: none !important;
        }
        
        [data-testid="stMetricValue"] {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif !important;
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 1.5rem !important;
            text-shadow: none !important;
        }
        
        /* === GENETIC DATA VISUALIZATION === */
        /* Futuristic genetic badge */
        .genetic-badge {
            background-color: #f5f5f5;
            padding: 0.75rem 1.25rem;
            border-radius: var(--border-radius-sm);
            display: inline-flex;
            align-items: center;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
            box-shadow: var(--box-shadow);
            transition: var(--transition);
            font-family: 'Share Tech Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            position: relative;
            overflow: hidden;
        }
        
        .genetic-badge::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 100%;
            background: none;
        }
        
        .genetic-badge:hover {
            box-shadow: var(--neon-glow-cyan);
        }
        
        .genetic-badge .icon {
            font-size: 1.25rem;
            margin-right: 0.75rem;
            color: var(--primary-color);
        }
        
        .genetic-badge .text {
            font-weight: 600;
            color: var(--primary-color);
            letter-spacing: 0.1em;
            font-size: 0.85rem;
        }
        
        /* Futuristic marker cards */
        .marker-card {
            background-color: #FFFFFF;
            border-radius: var(--border-radius);
            padding: 1.25rem;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
            box-shadow: var(--box-shadow);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .marker-card:hover {
            border-color: var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        .marker-card::after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--primary-color);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
            box-shadow: var(--neon-glow-cyan);
        }
        
        .marker-card:hover::after {
            transform: scaleX(1);
        }
        
        .marker-card .title {
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.75rem;
            font-size: 1.125rem;
            display: flex;
            align-items: center;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .marker-card .title::before {
            content: "⚛";
            margin-right: 0.75rem;
            font-size: 1.25rem;
            color: var(--primary-color);
        }
        
        /* === CUSTOM SIDEBAR NAVIGATION === */
        /* Futuristic sidebar styling */
        section[data-testid="stSidebar"] {
            background: var(--bg-secondary);
            border-right: 1px solid #e0e0e0; /* Light shade of gray border */
            box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5);
        }
        
        /* Futuristic navigation radio button styling */
        .stRadio > div {
            gap: 6px !important;
            display: flex;
            flex-direction: column;
        }
        
        /* Sidebar tabs styling - pill-shaped design */
        .stRadio > div {
            gap: 12px !important; /* Increased spacing between tabs */
        }
        
        .stRadio > div > label {
            padding: 12px 16px !important; /* Adjusted padding for pill shape */
            margin: 0 !important;
            border-radius: 50px !important; /* Pill shape */
            transition: all 0.2s ease !important;
            background-color: #FFFFFF !important; /* White background */
            color: #333333 !important; /* Dark gray text */
            border: none !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important; /* Subtle shadow */
            position: relative;
            overflow: hidden;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            font-size: 0.85rem !important;
            width: 100% !important; /* Full width */
            box-sizing: border-box !important;
            display: flex !important;
            align-items: center !important;
        }
        
        .stRadio > div > label:not(.stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label):hover {
            background-color: #F8F8F8 !important; /* Very light gray on hover */
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important; /* Slightly stronger shadow on hover */
            transform: translateY(-1px) !important; /* Slight lift effect */
        }
        
        /* Override hover styles for selected sidebar navigation items */
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label:hover {
            background-color: #FFFFFF !important; /* Keep white background for selected */
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Selected tab styling */
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label {
            background-color: #FFFFFF !important; /* White background */
            color: #333333 !important; /* Dark gray text */
            font-weight: 700 !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important; /* Slightly stronger shadow */
        }
        
        /* Red dot indicator for selected tab */
        .stRadio > div [data-baseweb="radio"] [data-checked="true"] ~ label:before {
            content: "";
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            background-color: #FF4B4B; /* Red dot */
            border-radius: 50%;
        }
        
        /* Add left padding for the icon space in all tabs */
        .stRadio > div > label {
            padding-left: 32px !important; /* Space for icon/indicator */
        }
        
        /* Style for the radio button text and icons */
        .stRadio [data-testid="stMarkdownContainer"] {
            font-size: 0.85rem !important;
            letter-spacing: 0.05em !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            font-family: 'Share Tech Mono', monospace !important;
            text-transform: uppercase !important;
            width: 100% !important;
        }
        
        /* Style for the icons in the radio buttons */
        .stRadio [data-testid="stMarkdownContainer"] code {
            font-family: inherit !important;
            background: none !important;
            padding: 0 !important;
            margin-right: 8px !important;
            color: inherit !important;
            border: none !important;
        }
        
        /* Hide the actual radio button circle and only keep the label */
        .stRadio [data-baseweb="radio"] [data-testid="stRadio"] {
            display: none !important;
        }
        
        /* Add a subtle pulsing glow effect to active menu item */
        @keyframes neo-pulse-glow {
            0% { box-shadow: 0 0 5px rgba(0, 240, 255, 0.5); }
            50% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.8), 0 0 20px rgba(0, 240, 255, 0.3); }
            100% { box-shadow: 0 0 5px rgba(0, 240, 255, 0.5); }
        }
        
        /* Removed animation from sidebar tabs */
        
        /* Futuristic sidebar section header */
        .sidebar-section {
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        }
        
        .sidebar-section h3 {
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.75rem;
            color: var(--primary-color);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            margin-left: 15px;
            position: relative;
            display: inline-block;
        }
        
        .sidebar-section h3::after {
            content: "";
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 1px;
            background: var(--primary-color);
            box-shadow: var(--neon-glow-cyan);
        }
        
        /* Futuristic info card in sidebar */
        .sidebar-info-card {
            background-color: white;
            border-radius: var(--border-radius);
            padding: 18px;
            margin: 15px 10px;
            border: 1px solid #e0e0e0; /* Light shade of gray border */
            box-shadow: var(--box-shadow);
        }
        

        
        .sidebar-info-card h4 {
            font-family: 'Orbitron', sans-serif;
            font-size:
        
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
            border: 1px solid #e0e0e0; /* Light shade of gray border */
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
            border: 1px solid #e0e0e0; /* Light shade of gray border */
            position: relative;
            overflow: hidden;
            box-shadow: var(--box-shadow);
        }
        
        .genetics-active-badge:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 0;
            background: none;
            opacity: 0;
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
        
        /* === FORCE LIGHT MODE === */
        /* Force light mode only - completely disable dark mode */
        /* Disable prefers-color-scheme media query entirely */
        @media (prefers-color-scheme: no-preference), (prefers-color-scheme: light), (prefers-color-scheme: dark) {
            :root {
                /* Light theme color palette - same as default */
                --primary-color: #00003c;  /* Dark navy blue */
                --primary-light: #0000a0;  /* Lighter navy blue */
                --primary-dark: #000020;  /* Darker navy blue */
                --accent-color: #7B42F6;  /* Neon purple */
                --warning-color: #FFD600;  /* Neon yellow */
                --success-color: #00FF94;  /* Neon green */
                --info-color: #00003c;  /* Dark navy blue */
                --error-color: #FF3D71;  /* Neon red */
                
                /* Text colors - forced to dark for better visibility on light backgrounds */
                --text-color: #333333;  /* Dark gray for text */
                --text-muted: #666666;  /* Medium gray for muted text */
                --text-light: #999999;  /* Light gray for light text */
                
                /* Background colors - forced to light */
                --bg-primary: #FFFFFF;  /* White background */
                --card-bg: #FFFFFF;  /* White card background */
                
                /* Glows and shadows - lighter for light mode */
                --neon-glow-cyan: 0 0 5px rgba(0, 0, 60, 0.3), 0 0 10px rgba(0, 0, 60, 0.2);
                --neon-glow-magenta: 0 0 5px rgba(255, 0, 228, 0.3), 0 0 10px rgba(255, 0, 228, 0.2);
                --neon-glow-purple: 0 0 5px rgba(123, 66, 246, 0.3), 0 0 10px rgba(123, 66, 246, 0.2);
                --neon-glow-yellow: 0 0 5px rgba(255, 214, 0, 0.3), 0 0 10px rgba(255, 214, 0, 0.2);
                --neon-glow-green: 0 0 5px rgba(0, 255, 148, 0.3), 0 0 10px rgba(0, 255, 148, 0.2);
                
                --box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
                --box-shadow-md: 0 4px 15px -3px rgba(0, 0, 0, 0.07);
                --box-shadow-lg: 0 8px 25px -5px rgba(0, 0, 0, 0.08);
                
                /* Sidebar specific - light colors */
                --sidebar-bg: #F0F0F0;
                --sidebar-element-bg: #FFFFFF;
                --sidebar-element-active-bg: linear-gradient(135deg, #64B5F6, #42A5F5);
                --sidebar-element-active-color: #FFFFFF;
                --sidebar-element-color: #333333;
                --sidebar-text-color: #333333;
                --sidebar-accent-color: #0066CC;
                --sidebar-badge-bg: rgba(100, 181, 246, 0.1);
                
                /* Form elements - light colors */
                --input-bg: #FFFFFF;
                --input-border: #E0E0E0;
                --input-text: #333333;
                --input-focus-border: #64B5F6;
                --input-focus-shadow: rgba(100, 181, 246, 0.2);
            }
            
            /* Force light mode for all elements */
            body, .main .block-container {
                background-color: #FFFFFF !important;
                color: #333333 !important;
            }
            
            /* Force light mode for all text */
            h1, h2, h3, h4, h5, h6, p, span, div, a, button, input, select, textarea {
                color: #333333 !important;
            }
            
            /* Force light backgrounds for all containers */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], 
            [data-testid="stSidebarContent"], .main, .block-container, 
            [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
                background-color: #FFFFFF !important;
            }
            
            /* Force light mode for tab panels */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: #f5f5f5 !important;
                color: #000000 !important;
            }
            
            /* Force light mode for all text in tab panels */
            .stTabs [data-baseweb="tab-panel"] *,
            .stTabs [data-baseweb="tab-panel"] p,
            .stTabs [data-baseweb="tab-panel"] span,
            .stTabs [data-baseweb="tab-panel"] div,
            .stTabs [data-baseweb="tab-panel"] h1,
            .stTabs [data-baseweb="tab-panel"] h2,
            .stTabs [data-baseweb="tab-panel"] h3,
            .stTabs [data-baseweb="tab-panel"] h4,
            .stTabs [data-baseweb="tab-panel"] h5,
            .stTabs [data-baseweb="tab-panel"] h6 {
                color: #000000 !important;
            }
            
            /* Force light mode for all cards and containers */
            .card-container, .plan-section, .health-assessment-section, .meal-card, .marker-card {
                background-color: #FFFFFF !important;
                border-color: #e0e0e0 !important;
            }
            
            /* Force light mode for all form elements */
            input, select, textarea, button,
            .stTextInput > div > div,
            .stSelectbox > div > div > div,
            .stNumberInput > div > div,
            .stTextArea > div > div,
            .stMultiSelect > div > div > div {
                background-color: #FFFFFF !important;
                color: #333333 !important;
                border-color: #e0e0e0 !important;
            }
            
            /* Force light mode for all metrics */
            [data-testid="stMetric"],
            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"] {
                background-color: #FFFFFF !important;
                color: #333333 !important;
            }
        }
        
        /* === THEME COLORS === */
        /* Force light mode only - completely disable dark mode */
        /* Target any dark mode elements and force light mode */
        @media (prefers-color-scheme: dark) {
            :root {
                /* Light theme color palette - same as default */
                --primary-color: #00003c;  /* Dark navy blue */
                --primary-light: #0000a0;  /* Lighter navy blue */
                --primary-dark: #000020;  /* Darker navy blue */
                --accent-color: #7B42F6;  /* Neon purple */
                --warning-color: #FFD600;  /* Neon yellow */
                --success-color: #00FF94;  /* Neon green */
                --info-color: #00003c;  /* Dark navy blue */
                --error-color: #FF3D71;  /* Neon red */
                
                /* Text colors - forced to dark for better visibility on light backgrounds */
                --text-color: #333333;  /* Dark gray for text */
                --text-muted: #666666;  /* Medium gray for muted text */
                --text-light: #999999;  /* Light gray for light text */
                
                /* Background colors - forced to light */
                --bg-primary: #FFFFFF;  /* White background */
                --card-bg: #FFFFFF;  /* White card background */
                
                /* Glows and shadows - lighter for light mode */
                --neon-glow-cyan: 0 0 5px rgba(0, 0, 60, 0.3), 0 0 10px rgba(0, 0, 60, 0.2);
                --neon-glow-magenta: 0 0 5px rgba(255, 0, 228, 0.3), 0 0 10px rgba(255, 0, 228, 0.2);
                --neon-glow-purple: 0 0 5px rgba(123, 66, 246, 0.3), 0 0 10px rgba(123, 66, 246, 0.2);
                --neon-glow-yellow: 0 0 5px rgba(255, 214, 0, 0.3), 0 0 10px rgba(255, 214, 0, 0.2);
                --neon-glow-green: 0 0 5px rgba(0, 255, 148, 0.3), 0 0 10px rgba(0, 255, 148, 0.2);
                
                --box-shadow: 0 2px 10px -2px rgba(0, 0, 0, 0.05);
                --box-shadow-md: 0 4px 15px -3px rgba(0, 0, 0, 0.07);
                --box-shadow-lg: 0 8px 25px -5px rgba(0, 0, 0, 0.08);
                
                /* Sidebar specific - light colors */
                --sidebar-bg: #F0F0F0;
                --sidebar-element-bg: #FFFFFF;
                --sidebar-element-active-bg: linear-gradient(135deg, #64B5F6, #42A5F5);
                --sidebar-element-active-color: #FFFFFF;
                --sidebar-element-color: #333333;
                --sidebar-text-color: #333333;
                --sidebar-accent-color: #0066CC;
                --sidebar-badge-bg: rgba(100, 181, 246, 0.1);
                
                /* Form elements - light colors */
                --input-bg: #FFFFFF;
                --input-border: #E0E0E0;
                --input-text: #333333;
                --input-focus-border: #64B5F6;
                --input-focus-shadow: rgba(100, 181, 246, 0.2);
            }
            
            /* Force light mode for all elements */
            body, .main .block-container {
                background-color: #FFFFFF !important;
                color: #333333 !important;
            }
            
            /* Force light mode for all text */
            h1, h2, h3, h4, h5, h6, p, span, div, a, button, input, select, textarea {
                color: #333333 !important;
            }
            
            /* Force light backgrounds for all containers */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], 
            [data-testid="stSidebarContent"], .main, .block-container, 
            [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
                background-color: #FFFFFF !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    """
    Configure and display the sidebar. Returns the current page selection.
    """
    # Add app title at the very top of the sidebar
    st.sidebar.markdown("""
    <div style="background: linear-gradient(90deg, #429de3, #87CEEB); 
                padding: 15px; 
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
        <h1 style="color: #000000; 
                font-family: 'Trebuchet MS', sans-serif;
                text-align: center;
                letter-spacing: 2px;
                font-weight: 600;
                text-transform: uppercase;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);">
                NEURO NUTRITION
        </h1>
    </div>
    """, unsafe_allow_html=True)
    


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
        {"id": "Health Assessment", "icon": "🫀", "text": "Health Assessment"},
        {"id": "Educational Resources", "icon": "📚", "text": "Resources"}
    ]
    
    # Instead of custom HTML navigation, use direct radio buttons with styling
    selected_page = st.sidebar.radio(
        "", 
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
        
        #Genetic insights info card
        st.sidebar.markdown("""
                            
        <h3 style="color:#000000;">About This App</h3>
                            
        <div class="sidebar-info-card">
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
        <h3 style="color:#000000;">About This App</h3>
        <div class="sidebar-info-card">
            <p>This application provides personalized nutrition guidance for individuals with diabetes, taking into account:</p>
            <ul>
                <li>Health metrics and diabetes status</li>
                <li>Socioeconomic context</li>
                <li>Genetic profile (optional)</li>
            </ul>
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
    # Add custom CSS to match the example image
    st.markdown("""
    <style>
    /* Style for the form container */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Style for input fields */
    .stNumberInput > div, 
    .stSelectbox > div,
    .stMultiSelect > div,
    .stTextArea > div {
        background-color: #f8f9fa !important;
        border-radius: 10px !important;
    }
    
    /* Style for input fields */
    .stNumberInput input,
    .stSelectbox input,
    .stMultiSelect input,
    .stTextArea textarea {
        background-color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px !important;
    }
    
    /* Style for the metric (BMI) */
    [data-testid="stMetric"] {
        background-color: white !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Style for labels */
    .stNumberInput label, 
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label {
        font-weight: 500 !important;
        color: #333 !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize health_data in session state if it doesn't exist
    previous_health_data = st.session_state.health_data.copy() if 'health_data' in st.session_state else {}

    if 'health_data' not in st.session_state:
        st.session_state.health_data = {}
    
    # Create a container with a light background and rounded corners
    with st.container():
        
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
                
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
                index=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"].index(st.session_state.activity_level),
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
                "Current Medications (separate by commas)",
                value=st.session_state.medications,
                key="medications_input",
                height=100
            )
            st.session_state.medications = medications
            
            if 'other_conditions' not in st.session_state:
                st.session_state.other_conditions = ""  # Default value
                
            other_conditions = st.text_area(
                "Other Health Conditions (separate by commas)",
                value=st.session_state.other_conditions,
                key="other_conditions_input",
                height=100
            )
            st.session_state.other_conditions = other_conditions

        # Close the container div
        st.markdown("</div>", unsafe_allow_html=True)
        
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
    # Add custom CSS to match the example image
    st.markdown("""
    <style>
    /* Style for the form container */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Style for input fields */
    .stNumberInput > div, 
    .stSelectbox > div,
    .stMultiSelect > div,
    .stTextArea > div,
    .stTextInput > div {
        background-color: #f8f9fa !important;
        border-radius: 10px !important;
    }
    
    /* Style for input fields */
    .stNumberInput input,
    .stSelectbox input,
    .stMultiSelect input,
    .stTextArea textarea,
    .stTextInput input {
        background-color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px !important;
    }
    
    
    /* Style for labels */
    .stNumberInput label, 
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stTextInput label {
        font-weight: 500 !important;
        color: #333 !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize socio_data in session state if it doesn't exist
    if 'socio_data' not in st.session_state:
        st.session_state.socio_data = {}
    
    # Create a container with a light background and rounded corners
    with st.container():
        
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
        'language_preferences': language_preferences,
        'literacy_level': literacy_level,
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
