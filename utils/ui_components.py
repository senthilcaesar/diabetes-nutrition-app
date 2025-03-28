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
        st.markdown('<h2 style="color:#379ced; font-size:35px;">Genetically Optimized Diabetes Nutrition Plan</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#757575;">Personalized nutrition recommendations based on your health metrics, socioeconomic context, and genetic profile</p>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color:#379ced; font-size:35px;">Personalized Diabetes Nutrition Plan</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#757575;">Personalized nutrition recommendations  based on your health metrics and socioeconomic context</p>', unsafe_allow_html=True)

def apply_custom_css():
    """
    Apply custom CSS styling to the application.
    """
    st.markdown("""
    <style>

        <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none !important;}
        
        /* Force the entire app to start from the very top */
        .stApp {
            margin-top: -4rem !important;
        }
        
        /* Make the app container take up full height with no padding */
        .appview-container {
            padding-top: 0 !important;
        }
        
        /* Adjust sidebar to start from the top edge with no extra space */
        section[data-testid="stSidebar"] {
            top: 0 !important;
            padding-top: 4rem !important; /* Compensation for negative margin */
        }
        
        /* Remove padding and margin from sidebar content */
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Adjust the Navigation header in sidebar */
        [data-testid="stSidebarContent"] h1:first-child,
        [data-testid="stSidebarContent"] h2:first-child,
        [data-testid="stSidebarContent"] h3:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Remove padding from main content area */
        .main .block-container {
            padding-top: 4rem !important; /* Compensation for negative margin */
        }
        
        /* Ensure nothing gets hidden behind the negative margin */
        body {
            overflow-x: hidden;
        }
                      
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none !important;}
        
        /* Force the entire app to start from the very top */
        .stApp {
            margin-top: -4rem !important;
        }
        
        /* Make the app container take up full height with no padding */
        .appview-container {
            padding-top: 0 !important;
        }
        
        /* Adjust sidebar to start from the top edge */
        section[data-testid="stSidebar"] {
            top: 0 !important;
            padding-top: 4rem !important; /* Add padding to account for negative margin */
        }
        
        /* Remove padding from main content area */
        .main .block-container {
            padding-top: 4rem !important; /* Add padding to account for negative margin */
        }
        
        /* Ensure nothing gets hidden behind the negative margin */
        body {
            overflow-x: hidden;
        }
                
        /* Hide Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Fix the empty space below tabs */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0px !important;
        }

        /* Remove padding around the container holding the tab panels */
        .stTabs [data-baseweb="tab-content"] {
            padding: 0px !important;
        }

        /* Make the card container start right at the top of the tab panel */
        .card-container {
            background-color: var(--background-color);
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 20px;
            margin-top: 0px !important;
            margin-bottom: 20px;
        }

        /* Tab styles */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 18px;
            background-color: var(--tab-background-color);
            color: var(--tab-color);
            border-radius: 6px 6px 0px 0px;
            border-left: 1px solid #eee;
            border-right: 1px solid #eee;
            border-top: 1px solid #eee;
            box-shadow: 0px -2px 5px rgba(0,0,0,0.05);
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--tab-selected-background-color) !important;
            color: var(--tab-selected-color) !important;
            font-weight: 600;
            border: none;
            transform: translateY(-3px);
            transition: all 0.3s ease;
        }

        /* Button styles */
        .nav-button {
            font-weight: 500 !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            transition: all 0.2s ease !important;
        }
        .nav-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }

        /* Message styles */
        .success-message {
            padding: 10px 15px;
            border-radius: 6px;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Section header styles */
        .section-header {
            margin-bottom: 1px;
            color: var(--section-header-color);
            font-size: 1.2rem;
            border-bottom: 1px solid var(--section-header-border-color);
            padding-bottom: 8px;
            display: inline-block;
        }

        /* Plan styling */
        .plan-header {
            background-color: var(--plan-header-background-color);
            padding: 20px;
            border-radius: 10px;
            color: var(--plan-header-color);
            margin-bottom: 20px;
            text-align: center;
        }
        .plan-section {
            background-color: var(--plan-section-background-color);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .plan-section h3 {
            color: var(--plan-section-header-color);
            border-bottom: 2px solid var(--plan-section-header-border-color);
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        .meal-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: var(--meal-card-background-color);
        }
        .meal-title {
            font-weight: bold;
            color: var(--meal-title-color);
            margin-bottom: 10px;
        }
                
        /* Foods limit section styles */
        .limit-section {
            background-color: var(--limit-section-background-color); /* Light yellow background */
            border-left: 4px solid var(--limit-section-border-color); /* Yellow border */
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .limit-section h2 {
            color: var(--limit-section-title-color); /* Orange-red color for title */
            font-weight: bold;
        }

        /* Health Assessment specific styling */
        .health-assessment-section {
            margin-bottom: 25px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .health-assessment-section h2 {
            font-size: 1.5rem;
            color: #2E7D32;
            margin-top: 0;
            margin-bottom: 15px;
            border-bottom: 2px solid #C8E6C9;
            padding-bottom: 8px;
        }

        .health-assessment-section h3 {
            font-size: 1.2rem;
            color: #1565C0;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        .health-assessment-section p {
            margin: 10px 0;
            line-height: 1.6;
            font-size: 1rem;
        }

        .summary-section {
            background-color: #E8F5E9;
            border-left: 5px solid #4CAF50;
        }

        .diabetes-management-section {
            background-color: #E3F2FD;
            border-left: 5px solid #2196F3;
        }


        .risks-section {
            background-color: #FFEBEE;
            border-left: 5px solid #F44336;
        }

        .care-plans-section {
            background-color: #E0F7FA;
            border-left: 5px solid #00BCD4;
        }

        .concerns-section {
            background-color: #FFF3E0;
            border-left: 5px solid #FF9800;
        }

        .recommendations-section {
            background-color: #F1F8E9;
            border-left: 5px solid #8BC34A;
        }

        .genetic-section {
            background-color: #E8EAF6;
            border-left: 5px solid #3F51B5;
        }


        /* Make paragraphs more readable */
        p {
            line-height: 1.6;
            margin-bottom: 15px;
        }

        /* Improve list formatting */
        ul, ol {
            margin-left: 20px;
            margin-bottom: 15px;
        }

        li {
            margin-bottom: 8px;
            line-height: 1.5;
        }

        /* Table styling */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }

        th {
            background-color: #E3F2FD;
            padding: 10px;
            border: 1px solid #BBDEFB;
            font-weight: bold;
            text-align: left;
        }

        td {
            padding: 8px 10px;
            border: 1px solid #E3F2FD;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .health-assessment-section {
                padding: 15px;
            }
            
            .health-assessment-section h2 {
                font-size: 1.3rem;
            }
            
            .metric-item {
                padding: 10px;
            }
        }

        /* Serene Blue Light Mode */
        @media (prefers-color-scheme: light) {
            :root {
                --background-color: #f9f9f9;
                --tab-background-color: #e8e8e8;
                --tab-color: #555555;
                --tab-selected-background-color: #5cacee;
                --tab-selected-color: #ffffff;
                --section-header-color: #333333;
                --section-header-border-color: #5cacee;
                --plan-header-background-color: #5cacee;
                --plan-header-color: #ffffff;
                --plan-section-background-color: #ffffff;
                --plan-section-header-color: #333333;
                --plan-section-header-border-color: #5cacee;
                --meal-card-background-color: #f0f8ff;
                --meal-title-color: #1e90ff;
                --limit-section-background-color: #fff8e1;
                --limit-section-border-color: #ffecb3;
                --limit-section-title-color: #ffb300;
            }
        }

        /* Serene Blue Dark Mode (Revised Unselected Tabs - Light Background) */
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #303030;
                --tab-background-color: #4a5568;
                --tab-color: #d1d5db;
                --tab-selected-background-color: #61d46d;
                --tab-selected-color: #212121;
                --section-header-color: #f5f5f5;
                --section-header-border-color: #64b5f6;
                --plan-header-background-color: #64b5f6;
                --plan-header-color: #212121;
                --plan-section-background-color: #424242;
                --plan-section-header-color: #f5f5f5;
                --plan-section-header-border-color: #64b5f6;
                --meal-card-background-color: #4a4a4a;
                --meal-title-color: #90caf9;
                --limit-section-background-color: #5e5e5e;
                --limit-section-border-color: #757575;
                --limit-section-title-color: #ffea00;
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
    
    # Add a header directly above the navigation
    st.sidebar.header("Navigation")
    
    # Create radio button based on current page with a unique key and no label
    selected_page = st.sidebar.radio(
        "Navigation Options", 
        ["Input Data", "Nutrition Plan", "Health Assessment", "Educational Resources"],
        index=["Input Data", "Nutrition Plan", "Health Assessment", "Educational Resources"].index(st.session_state.page),
        key="navigation_radio",
        label_visibility="collapsed"  # Hide the empty label completely
    )
    
    # Only update if selected page is different from current
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()
    
    # Show genetic status if available
    if 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None:
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            """
            <div style="
                background-color: #E8EAF6; 
                padding: 10px; 
                border-radius: 5px;
                margin-bottom: 10px;
                text-align: center;
            ">
                <div style="font-size: 24px;">🧬</div>
                <div style="font-weight: bold; color: #3F51B5;">Genetic Optimization Active</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This application provides accessible, personalized nutrition guidance for individuals with diabetes, taking into account:
    
    - Health metrics and diabetes status
    - Socioeconomic context and resources
    - Cultural food preferences
    - Genetic profile (if provided)
    """)
    
    if 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None:
        st.sidebar.markdown("""
        ### Genetic Insights
        The nutrition plan and health assessment are enhanced with insights from your genetic profile, including:
        
        - Carbohydrate metabolism
        - Fat sensitivity
        - Nutrient processing
        - Inflammation response
        - Caffeine metabolism
        """)
        
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
        ### Enhance Your Assessment
        Upload genetic data on the Input Data page to receive more personalized recommendations tailored to your unique genetic profile.
        """)
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Developed by:")
    st.sidebar.markdown("Senthil Palanivelu")
    
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