import streamlit as st
import matplotlib.pyplot as plt
import time
import openai
from openai import OpenAI
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Wedge, Polygon

# Add at the top of app.py
from utils.data_processing import preprocess_health_data, preprocess_socioeconomic_data

# OpenAI API configuration
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store this securely in Streamlit secrets

# Set page configuration
st.set_page_config(
    page_title="Personalized Diabetes Nutrition Plan",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def generate_health_assessment(user_data):
    """Generate a health assessment using OpenAI API based on user health data."""
    prompt = create_health_assessment_prompt(user_data)
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",  # Use GPT-4 for more comprehensive medical analysis
        messages=[
            {"role": "system", "content": """
            You are an expert medical doctor specialized in diabetes and metabolic health assessment. 
            Provide a thorough assessment of the patient's health condition based on their data.
            Focus on diabetes management, identify potential risks, suggest diagnosis and generate care plans.
            
            Important rules:
            1. DO NOT make definitive diagnoses - only highlight potential concerns
            2. ALWAYS qualify your assessment with appropriate disclaimers about AI limitations
            3. Focus on objective measures and evidence-based recommendations
            4. Indicate clearly when values are outside of optimal ranges
            5. Prioritize the most critical health concerns first
            """
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Lower temperature for more consistent medical information
        max_tokens=1500
    )
    
    health_assessment = response.choices[0].message.content.strip()
    return health_assessment

def create_health_assessment_prompt(user_data):
    """Create a prompt for generating a health assessment."""
    
    # Extract and format key health metrics
    age = user_data.get('age', '')
    gender = user_data.get('gender', '')
    weight = user_data.get('weight', '')
    height = user_data.get('height', '')
    bmi = user_data.get('bmi', '')
    activity_level = user_data.get('activity_level', '')
    diabetes_type = user_data.get('diabetes_type', '')
    fasting_glucose = user_data.get('fasting_glucose', '')
    postmeal_glucose = user_data.get('postmeal_glucose', '')
    hba1c = user_data.get('hba1c', '')
    
    # Format medications and other conditions for better prompt structure
    medications = user_data.get('medications', '')
    medications_list = [med.strip() for med in medications.split('\n') if med.strip()]
    
    other_conditions = user_data.get('other_conditions', '')
    conditions_list = [condition.strip() for condition in other_conditions.split('\n') if condition.strip()]
    
    # Get dietary restrictions
    dietary_restrictions = user_data.get('dietary_restrictions', 'None')
    
    # Build the prompt
    prompt = f"""
    Please provide a comprehensive health assessment for a patient with the following profile:
    
    ## Basic Information
    - Age: {age}
    - Gender: {gender}
    - Weight: {weight} kg
    - Height: {height} cm
    - BMI: {bmi}
    - Activity Level: {activity_level}
    
    ## Diabetes Information
    - Diabetes Type: {diabetes_type}
    - Fasting Blood Glucose: {fasting_glucose} mg/dL
    - Post-meal Blood Glucose: {postmeal_glucose} mg/dL
    - HbA1c: {hba1c}%
    
    ## Medications
    {chr(10).join(f"- {med}" for med in medications_list) if medications_list else "- None specified"}
    
    ## Other Health Conditions
    {chr(10).join(f"- {condition}" for condition in conditions_list) if conditions_list else "- None specified"}
    
    ## Dietary Restrictions
    - {dietary_restrictions}
    
    ## Requested Assessment
    Please provide:
    1. An overall evaluation of the patient's diabetes management
    2. Analysis of their key metrics and how they compare to recommended targets
    3. Identification of potential health risks based on their profile
    4. Specific areas of concern that should be discussed with a healthcare provider
    5. Recommendations for improving their health management
    
    Format the assessment in clear sections with headings, and begin with a summary of the most important points.
    """
    
    return prompt

# Define helper functions for data preprocessing
def preprocess_health_data(health_data):
    """Preprocess and validate health data."""
    processed_data = health_data.copy()
    
    # Convert values to appropriate types
    for key in ['age', 'weight', 'height']:
        if key in processed_data and processed_data[key]:
            processed_data[key] = float(processed_data[key])
    
    # Calculate BMI if height and weight are available
    if all(key in processed_data and processed_data[key] for key in ['weight', 'height']):
        height_m = processed_data['height'] / 100  # Convert cm to m
        processed_data['bmi'] = round(processed_data['weight'] / (height_m ** 2), 1)
    
    # Convert glucose values to float
    for key in ['fasting_glucose', 'postmeal_glucose', 'hba1c']:
        if key in processed_data and processed_data[key]:
            processed_data[key] = float(processed_data[key])
    
    return processed_data

def preprocess_socioeconomic_data(socio_data):
    """Preprocess and validate socioeconomic data."""
    processed_data = socio_data.copy()
    
    # Determine plan complexity level based on education and literacy
    if 'education_level' in processed_data and 'literacy_level' in processed_data:
        edu = processed_data['education_level'].lower() if processed_data['education_level'] else ''
        lit = processed_data['literacy_level'].lower() if processed_data['literacy_level'] else ''
        
        if ('elementary' in edu or 'primary' in edu or 'low' in lit or 'basic' in lit):
            processed_data['plan_complexity'] = 'simple'
        elif ('high school' in edu or 'secondary' in edu or 'moderate' in lit or 'average' in lit):
            processed_data['plan_complexity'] = 'moderate'
        elif ('college' in edu or 'university' in edu or 'bachelor' in edu or 'master' in edu or 'doctorate' in edu or 'high' in lit):
            processed_data['plan_complexity'] = 'advanced'
        else:
            processed_data['plan_complexity'] = 'moderate'  # Default to moderate
    
    # Format guidance based on literacy and technology access
    if 'literacy_level' in processed_data and 'technology_access' in processed_data:
        lit = processed_data['literacy_level'].lower() if processed_data['literacy_level'] else ''
        tech = processed_data['technology_access'].lower() if processed_data['technology_access'] else ''
        
        if 'low' in lit or 'basic' in lit:
            processed_data['format_guidance'] = 'highly visual with minimal text'
        elif 'limited' in tech:
            processed_data['format_guidance'] = 'printable with visual aids'
        else:
            processed_data['format_guidance'] = 'balanced text and visuals'
    
    return processed_data

# AI Generation Functions
def generate_nutrition_plan(user_data):
    """Generate a personalized nutrition plan using OpenAI."""
    prompt = create_nutrition_plan_prompt(user_data)
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",  # Adjust based on availability and needs
        messages=[
            {"role": "system", "content": "You are a medical nutrition specialist with expertise in diabetes management. Create a personalized nutrition plan based on the provided health and socioeconomic data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    nutrition_plan = response.choices[0].message.content.strip()
    print(nutrition_plan)
    return nutrition_plan

def create_nutrition_plan_prompt(user_data):
    """Create a prompt for generating a nutrition plan."""
    diabetes_type = user_data.get('diabetes_type', 'Type 2')
    format_guidance = user_data.get('format_guidance', 'balanced text and visuals')
    plan_complexity = user_data.get('plan_complexity', 'moderate')
    cultural_foods = user_data.get('cultural_foods', 'No specific cultural preferences')
    literacy_level = user_data.get('literacy_level', 'moderate')
    income_level = user_data.get('income_level', 'medium')
    grocery_budget = user_data.get('grocery_budget', 'moderate')
    local_foods = user_data.get('local_food_availability', 'moderate')
    
    health_info = f"""
    ## Health Data
    - Age: {user_data.get('age')}
    - Gender: {user_data.get('gender')}
    - Weight (kg): {user_data.get('weight')}
    - Height (cm): {user_data.get('height')}
    - BMI: {user_data.get('bmi')}
    - Activity Level: {user_data.get('activity_level')}
    - Diabetes Type: {diabetes_type}
    - Blood Glucose Levels:
        - Fasting: {user_data.get('fasting_glucose')} mg/dL
        - Post-meal average: {user_data.get('postmeal_glucose')} mg/dL
    - HbA1c: {user_data.get('hba1c')}%
    - Dietary Restrictions: {user_data.get('dietary_restrictions')}
    - Current Medications: {user_data.get('medications')}
    - Other Health Conditions: {user_data.get('other_conditions')}
    """
    
    socio_info = f"""
    ## Socioeconomic Considerations
    - Format Guidance: {format_guidance}
    - Plan Complexity: {plan_complexity}
    - Cultural Food Preferences: {cultural_foods}
    - Literacy Level: {literacy_level}
    - Income Level: {income_level}
    - Grocery Budget: {grocery_budget}
    - Local Food Availability: {local_foods}
    - Location: {user_data.get('location')}
    - Geographic Setting: {user_data.get('geographic_setting')}
    - Cooking Facilities: {user_data.get('cooking_facilities')}
    - Time for Meal Preparation: {user_data.get('meal_prep_time')}
    """
    
    prompt = f"""
    Create a comprehensive, personalized nutrition plan for an individual with {diabetes_type} diabetes based on the following data:
    
    {health_info}
    
    {socio_info}
    
    ## Plan Specifications
    Please create a nutrition plan that includes:
    
    1. Daily caloric target and macronutrient distribution (carbs, protein, fat)
    2. Recommended meal structure (timing and composition)
    3. A sample 3-day meal plan with specific locally available foods
    4. Simple recipe ideas that require minimal preparation time and basic cooking facilities
    5. Guidance on proper portion sizes using common household items as references
    6. Specific foods to avoid or limit
    7. Foods that can help stabilize blood sugar
    
    The plan should be:
    - Culturally appropriate and incorporate local food options
    - Affordable within the specified budget
    - Easy to understand with the specified literacy level in mind
    - Practical considering the individual's living conditions and cooking facilities
    - Specifically designed to help manage diabetes while addressing other health conditions
    
    {'' if plan_complexity != 'simple' else 'Make the plan extremely simple, using basic language, visual cues, and minimal text. Focus on practical, actionable guidance rather than detailed explanations.'}
    
    {'' if plan_complexity != 'advanced' else 'Include more detailed nutritional information, rationale for recommendations, and guidance on adapting the plan as needed.'}
    
    {'' if 'visual' not in format_guidance else 'Design the plan to be highly visual with food images, simple icons, and minimal text. Use color coding to indicate foods that are encouraged (green), to be consumed in moderation (yellow), or to be limited/avoided (red).'}
    
    Return the plan in a well-formatted structure with clear sections.
    """
    
    return prompt

def generate_visual_guidance(nutrition_plan, literacy_level, plan_complexity):
    """Generate visual guidance descriptions based on the nutrition plan."""
    prompt = f"""
    Create detailed descriptions for visual aids to accompany the following nutrition plan:
    
    NUTRITION PLAN:
    {nutrition_plan}
    
    The user has a {literacy_level} literacy level and the plan complexity is {plan_complexity}.
    
    For each key concept in the nutrition plan, describe a simple, clear visual that could help communicate the information. These visual descriptions should:
    
    1. Focus on concrete representations of abstract concepts
    2. Use familiar objects, symbols, and scenarios
    3. Employ color coding for categorization (e.g., green for "good" foods, red for "avoid" foods)
    4. Include visual portion guides using common household objects
    5. Illustrate meal timing and structure
    6. Show cause-and-effect relationships related to food and blood sugar
    
    {'Include detailed visual descriptions that represent key information with minimal reliance on text.' if 'low' in literacy_level else 'Balance visual elements with text to reinforce key concepts.'}
    
    Provide 5-7 detailed visual descriptions covering the most important aspects of the nutrition plan.
    
    For each visual, provide:
    1. A clear title
    2. A detailed description of what the visual should look like
    3. The key message this visual is meant to convey
    """
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a visual health educator specialized in creating accessible diabetes education materials."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    
    visual_guidance = response.choices[0].message.content.strip()
    return visual_guidance

# Function to navigate to view plan page
def navigate_to_view_plan():
    st.session_state.page = "Nutrition Plan"

# UI Components
def show_header():
    """Display the application header."""

    st.markdown('<h2 style="color:#1E88E5; font-size:35px;">Personalized Diabetes Nutrition Plan</h2>', unsafe_allow_html=True)
    #st.markdown("""
    #This application creates personalized nutrition plans for individuals with diabetes, 
    #taking into account health metrics, socioeconomic factors, and cultural preferences.
    #""")
    #st.markdown("---")


def input_health_data():
    """Collect health-related data from the user and save to session state."""
    # Initialize health_data in session state if it doesn't exist
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
    """Collect socioeconomic data from the user using dropdown menus and save to session state."""
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
        
        # Income Level - Changed from slider to selectbox
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
        
        # Literacy Level - Changed from slider to selectbox
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
        
        # Technology Access - Changed from slider to selectbox
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
        
        # Healthcare Access - Changed from slider to selectbox
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
        
        # Grocery Budget - Changed from slider to selectbox
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
        
        # Meal Prep Time - Changed from slider to selectbox
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

def show_input_data_page():
    # Add more aggressive CSS to fix the empty space below tabs
    # Add some custom CSS for better styling
    st.markdown("""
    <style>
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
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 20px;
            margin-top: 0px !important;
            margin-bottom: 20px;
        }
        
        /* Other styles remain the same */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px;
            background-color: #f8f9fa;
            border-radius: 6px 6px 0px 0px;
            border-left: 1px solid #eee;
            border-right: 1px solid #eee;
            border-top: 1px solid #eee;
            box-shadow: 0px -2px 5px rgba(0,0,0,0.05);
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: 600;
            border: none;
            transform: translateY(-3px);
            transition: all 0.3s ease;
        }
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
        .success-message {
            padding: 10px 15px;
            border-radius: 6px;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .section-header {
            margin-bottom: 1px;
            color: #2C3E50;
            font-size: 1.2rem;
            border-bottom: 1px solid #4CAF50;
            padding-bottom: 8px;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create tabs with a different approach
    tab_titles = ["🩺 Health Information", "🏘️ Socioeconomic Information", "🚀 Generate Plan"]
    tabs = st.tabs(tab_titles)
    
    with tabs[0]:
        st.markdown("")
        # Start with no whitespace at all
        #st.markdown('<div class="card-container">', unsafe_allow_html=True)
        #st.markdown('<h3 class="section-header">Your Health Profile</h3>', unsafe_allow_html=True)
        
        # Add a brief introduction
        #st.markdown("""
        #Please provide your health information to help us create a personalized nutrition plan 
        #tailored to your specific needs. This information will be used to calculate appropriate
        #calorie and nutrient targets.
        #""")
        
        if 'health_data' not in st.session_state:
            st.session_state.health_data = {}
        
        st.session_state.health_data = input_health_data()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Save Health Information", key="save_health", use_container_width=True, 
                        type="primary", help="Save your health information and proceed to the next tab"):
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("Health information saved! Please proceed to the Socioeconomic Information tab.")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("")
        #st.markdown('<div class="card-container">', unsafe_allow_html=True)
        #st.markdown('<h3 class="section-header">Your Living Context</h3>', unsafe_allow_html=True)
        
        # Add a brief introduction
        #st.markdown("""
        #Understanding your living situation, cultural context, and resources helps us create 
        #a nutrition plan that's practical and accessible for your specific circumstances.
        #""")
        
        if 'socio_data' not in st.session_state:
            st.session_state.socio_data = {}
        
        st.session_state.socio_data = input_socioeconomic_data()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Save Socioeconomic Information", key="save_socio", use_container_width=True, 
                        type="primary", help="Save your socioeconomic information and proceed to generate plan"):
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success("Socioeconomic information saved! Please proceed to the Generate Plan tab.")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("")
        #st.markdown('<div class="card-container">', unsafe_allow_html=True)
        #st.markdown('<h3 class="section-header">Generate Your Personalized Plan</h3>', unsafe_allow_html=True)
        
        if 'health_data' in st.session_state and 'socio_data' in st.session_state:
            st.info("You're almost there! Review your information before generating your personalized nutrition plan.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_button = st.button("📋 Review Your Data", use_container_width=True, 
                                      help="View the information you've provided")
            with col2:
                generate_button = st.button("✨ Create My Nutrition Plan", key="generate_plan", 
                                          use_container_width=True, type="primary",
                                          help="Generate your personalized nutrition plan based on your information")
            
            if show_button:
                st.write("")  # Add a little spacing
                
                health_tab, socio_tab = st.tabs(["Health Data", "Socioeconomic Data"])
                
                with health_tab:
                    # Format the health data in a more readable way
                    st.subheader("Your Health Information")
                    health_data = st.session_state.health_data
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Age:**", health_data.get('age'))
                        st.write("**Gender:**", health_data.get('gender'))
                        st.write("**Weight:**", health_data.get('weight'), "kg")
                        st.write("**Height:**", health_data.get('height'), "cm")
                        st.write("**BMI:**", health_data.get('bmi'))
                    
                    with col2:
                        st.write("**Diabetes Type:**", health_data.get('diabetes_type'))
                        st.write("**HbA1c:**", health_data.get('hba1c'), "%")
                        st.write("**Fasting Glucose:**", health_data.get('fasting_glucose'), "mg/dL")
                        st.write("**Activity Level:**", health_data.get('activity_level'))
                        st.write("**Dietary Restrictions:**", health_data.get('dietary_restrictions')[:50] + "..." if len(health_data.get('dietary_restrictions', '')) > 50 else health_data.get('dietary_restrictions', ''))
                        

                        # Get the medications
                        medications = health_data.get('medications', '')

                        # Format for display - replace newlines with commas and add proper spacing
                        if medications:
                            # Replace newlines with commas for display
                            formatted_medications = medications.replace('\n', ', ').replace(',,', ',').strip(',')
                            
                            # Truncate if too long
                            if len(formatted_medications) > 50:
                                display_text = formatted_medications[:50] + "..."
                            else:
                                display_text = formatted_medications
                                
                            st.write("**Current Medications:**", display_text)
                        else:
                            st.write("**Current Medications:** None")

                        # Get the other conditions
                        other_conditions = health_data.get('other_conditions', '')

                        # Format for display - remove trailing commas and add proper spacing
                        if other_conditions:
                            # Replace newlines with commas for display
                            formatted_conditions = other_conditions.replace('\n', ', ').replace(',,', ',').strip(',')
                            
                            # Truncate if too long
                            if len(formatted_conditions) > 50:
                                display_text = formatted_conditions[:50] + "..."
                            else:
                                display_text = formatted_conditions
                                
                            st.write("**Other Health Conditions:**", display_text)
                        else:
                            st.write("**Other Health Conditions:** None")


                with socio_tab:
                    # Format the socioeconomic data in a more readable way
                    st.subheader("Your Socioeconomic Information")
                    socio_data = st.session_state.socio_data
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Location:**", socio_data.get('location'))
                        st.write("**Setting:**", socio_data.get('geographic_setting'))
                        st.write("**Income Level:**", socio_data.get('income_level'))
                        st.write("**Education Level:**", socio_data.get('education_level'))
                    
                    with col2:
                        st.write("**Food Availability:**", socio_data.get('local_food_availability'))
                        st.write("**Cooking Facilities:**", socio_data.get('cooking_facilities'))
                        st.write("**Meal Prep Time:**", socio_data.get('meal_prep_time'))
                        st.write("**Cultural Foods:**", socio_data.get('cultural_foods')[:50] + "..." if len(socio_data.get('cultural_foods', '')) > 50 else socio_data.get('cultural_foods', ''))
            
            if generate_button:
                # Create a placeholder for the header text
                header_placeholder = st.empty()
                header_placeholder.markdown("""
                <div style="text-align: center; padding: 10px;">
                    <h3>Crafting Your Personalized Nutrition Plan</h3>
                    <p>Analyzing your health data and creating customized recommendations...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Create a percentage text placeholder
                percentage_text = st.empty()
                
                # Use the Streamlit spinner for the animation
                with st.spinner(""):
                    # Simulate progress up to 90% (reserve the last 10% for actual generation)
                    for percent_complete in range(0, 91, 10):
                        # Update progress bar
                        progress_bar.progress(percent_complete/100)
                        # Update percentage text
                        percentage_text.markdown(f"<div style='text-align: center;'><strong>{percent_complete}% Complete</strong></div>", unsafe_allow_html=True)
                        # Add a small delay to simulate processing
                        time.sleep(0.5)  # Adjust as needed
                    
                    # Preprocess the data
                    processed_health_data = preprocess_health_data(st.session_state.health_data)
                    progress_bar.progress(92/100)
                    percentage_text.markdown("<div style='text-align: center;'><strong>92% Complete</strong></div>", unsafe_allow_html=True)
                    
                    processed_socio_data = preprocess_socioeconomic_data(st.session_state.socio_data)
                    progress_bar.progress(95/100)
                    percentage_text.markdown("<div style='text-align: center;'><strong>95% Complete</strong></div>", unsafe_allow_html=True)
                    
                    # Combine the data
                    combined_data = {**processed_health_data, **processed_socio_data}
                    
                    # Generate the nutrition plan
                    try:
                        # Generate plan
                        nutrition_plan = generate_nutrition_plan(combined_data)
                        st.session_state.nutrition_plan = nutrition_plan
                        progress_bar.progress(98/100)
                        percentage_text.markdown("<div style='text-align: center;'><strong>98% Complete</strong></div>", unsafe_allow_html=True)
                        
                        # Generate visual guidance
                        visual_guidance = generate_visual_guidance(
                            nutrition_plan, 
                            combined_data.get('literacy_level', 'moderate'),
                            combined_data.get('plan_complexity', 'moderate')
                        )
                        st.session_state.visual_guidance = visual_guidance
                        
                        # Show 100% completion
                        progress_bar.progress(100/100)
                        percentage_text.markdown("<div style='text-align: center;'><strong>100% Complete!</strong></div>", unsafe_allow_html=True)
                        
                        # Clear progress elements
                        time.sleep(0.5)
                        header_placeholder.empty()
                        progress_bar.empty()
                        percentage_text.empty()
                        
                        # Show completion animation
                        st.balloons()
                        st.success("✅ Your personalized nutrition plan has been generated!")
                        
                        # Add button to navigate to View Plan page
                        if st.button("View My Nutrition Plan →", type="primary", key="view_plan_button", 
                                    use_container_width=True, on_click=navigate_to_view_plan):
                            pass  # The on_click function handles the navigation
                            
                    except Exception as e:
                        # Clear progress elements
                        header_placeholder.empty()
                        progress_bar.empty()
                        percentage_text.empty()
                        
                        st.error(f"An error occurred while generating the plan: {str(e)}")
        else:
            # Create a more visually appealing warning
            st.markdown("""
            <div style="
                background-color: #FFF3E0; 
                padding: 15px; 
                border-left: 5px solid #FF9800;
                border-radius: 4px;
                margin: 10px 0;
            ">
                <h4 style="color: #E65100; margin-top: 0;">Information Needed</h4>
                <p>Please complete both the Health Information and Socioeconomic Information tabs before generating a plan.</p>
                <p>Click on the tabs above to enter your information.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add some helpful guidance images
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 48px;">🩺</div>
                    <h4>Step 1: Enter Health Information</h4>
                    <p>Share your health metrics to help us customize your plan.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 48px;">🏘️</div>
                    <h4>Step 2: Enter Socioeconomic Information</h4>
                    <p>Tell us about your lifestyle and resources for practical recommendations.</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)




# Update sidebar function to include the new page
def show_sidebar():
    """Configure and display the sidebar."""
    with st.sidebar:
        st.header("Navigation")
        
        # Initialize the page state if it doesn't exist
        if 'page' not in st.session_state:
            st.session_state.page = "Input Data"
        
        # Check for navigation request flag
        if 'nav_to_input' in st.session_state and st.session_state.nav_to_input:
            st.session_state.page = "Input Data"
            # Clear the flag
            st.session_state.nav_to_input = False
        
        # Create radio button based on current page with additional Health Assessment option
        selected_page = st.radio(
            "Go to", 
            ["Input Data", "Nutrition Plan", "Health Assessment", "Educational Resources"],  # Added Health Assessment
            index=["Input Data", "Nutrition Plan", "Health Assessment", "Educational Resources"].index(st.session_state.page)
        )
        
        # Only update if selected page is different from current
        if selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()
            
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application was developed to provide accessible, 
        personalized nutrition guidance for individuals with diabetes, 
        particularly those in underserved communities.
        """)
        
        st.markdown("---")
        st.markdown("### Developed by:")
        st.markdown("Senthil Palanivelu")
    
    return st.session_state.page

def show_nutrition_plan():
    """Display the generated nutrition plan."""
    if 'nutrition_plan' not in st.session_state:
        st.warning("No nutrition plan has been generated yet. Please go to the Input Data page first.")
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="primary", use_container_width=False):
            # Set a navigation flag instead of directly changing radio value
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
    # Add some CSS for better styling
    st.markdown("""
    <style>
        .plan-header {
            background-color: #4CAF50;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
            text-align: center;
        }
        .plan-section {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .plan-section h3 {
            color: #2C3E50;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        .meal-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        }
        .meal-title {
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
        }
                
        /* New styles for highlighted limit section */
        .limit-section {
            background-color: #FFF9C4; /* Light yellow background */
            border-left: 4px solid #FFC107; /* Yellow border */
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .limit-section h2 {
            color: #FF5722; /* Orange-red color for title */
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display header
    #st.markdown("""
    #<div class="plan-header">
    #    <h1>Your Personalized Diabetes Nutrition Plan</h1>
    #    <p>Created based on your unique health profile and living context</p>
    #</div>
    #""", unsafe_allow_html=True)
    
    # Display the plan in tabs for better organization
    overview_tab, meal_plan_tab, recipes_tab, visuals_tab = st.tabs(["Overview", "Meal Plan", "Recipes & Tips", "Visual Guides"])
    
    # Split the nutrition plan into sections
    nutrition_plan = st.session_state.nutrition_plan
    if "\n## " in nutrition_plan:
        sections = nutrition_plan.split("\n## ")
        sections = ["## " + section if i > 0 else section for i, section in enumerate(sections)]
    else:
        sections = nutrition_plan.split("\n### ")
        sections = ["### " + section if i > 0 else section for i, section in enumerate(sections)]

    
    # Extract main sections
    overview_sections = [s for s in sections if any(x in s.lower() for x in ["introduction", "overview", "caloric", "macronutrient", "recommended"])]
    meal_plan_sections = [s for s in sections if any(x in s.lower() for x in ["meal plan", "sample meal", "day 1", "day 2", "day 3"])]
    recipe_sections = [s for s in sections if any(x in s.lower() for x in ["recipe", "tips", "avoid", "limit", "portion", "guideline", "stabilize"])]
    
    with overview_tab:
        for section in overview_sections:
            st.markdown(section)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with meal_plan_tab:
        for section in meal_plan_sections:
                st.markdown(section)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with recipes_tab:
        for section in recipe_sections:
                st.markdown(section)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with visuals_tab:
        if 'visual_guidance' in st.session_state:
            # Get user preferences from health_data if available
            health_data = st.session_state.health_data
            
            # Extract relevant preferences
            food_preferences = health_data.get('food_preferences', [])
            dietary_restrictions_str = health_data.get('dietary_restrictions', '')
            dietary_restrictions = [restriction.strip() for restriction in dietary_restrictions_str.split(',') if restriction.strip()]
        
            cultural_preferences = health_data.get('cultural_preferences', '')
            
            # Create a more visually appealing portion guide with personalization
            def create_enhanced_portion_guide():
                try:
                    # Import necessary components
                    from matplotlib.patches import Wedge, Circle
                    
                    # Create figure with a nice background
                    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#f8f9fa')
                    ax.set_facecolor('#f8f9fa')
                    
                    # Draw the plate
                    plate = Circle((0.5, 0.5), 0.4, fill=True, color='#FFFFFF', ec='#333333', linewidth=2)
                    ax.add_patch(plate)
                    
                    # Create the plate sections
                    # Left half - vegetables
                    veg_wedge = Wedge((0.5, 0.5), 0.4, 90, 270, color='#81c784', alpha=0.7)  # Green for vegetables
                    ax.add_patch(veg_wedge)
                    
                    # Top right - proteins
                    protein_wedge = Wedge((0.5, 0.5), 0.4, 270, 0, color='#ffb74d', alpha=0.7)  # Orange for proteins
                    ax.add_patch(protein_wedge)
                    
                    # Bottom right - carbs
                    carb_wedge = Wedge((0.5, 0.5), 0.4, 0, 90, color='#64b5f6', alpha=0.7)  # Blue for carbs
                    ax.add_patch(carb_wedge)
                    
                    # Add section labels with icons
                    ax.text(0.35, 0.6, "NON-STARCHY\nVEGETABLES\n(50%)", ha='center', va='center', fontweight='bold', color='#1b5e20')
                    ax.text(0.70, 0.75, "PROTEINS\n(25%)", ha='center', va='center', fontweight='bold', color='#e65100')
                    ax.text(0.75, 0.25, "CARBS\n(25%)", ha='center', va='center', fontweight='bold', color='#0d47a1')
                    
                    # Customize food examples based on user preferences and restrictions
                    # Vegetables
                    veg_examples = ["Broccoli", "Spinach", "Peppers", "Tomatoes", "Zucchini"]
                    # Check if user has specified vegetable preferences
                    if dietary_restrictions and ("vegetarian" in dietary_restrictions or "vegan" in dietary_restrictions):
                        veg_examples = ["Broccoli", "Spinach", "Kale", "Bell Peppers", "Cauliflower"]
                    elif food_preferences and "Low vegetable intake" in food_preferences:
                        veg_examples = ["Carrots", "Tomatoes", "Cucumber", "Corn", "Green Beans"]
                    
                    # Proteins
                    protein_examples = ["Chicken", "Fish", "Beans", "Tofu", "Eggs", "Legumes", "Greek Yogurt"]
                    # Customize protein examples based on dietary restrictions
                    if dietary_restrictions:
                        if "Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions:
                            protein_examples = ["Tofu", "Beans", "Lentils", "Eggs", "Greek Yogurt", "Legumes", "Whole Grains"]
                    
                    # Carbs
                    carb_examples = ["Brown rice", "Sweet potato", "Quinoa", "Whole grain bread"]
                    # Customize carb examples based on preferences
                    if dietary_restrictions and "gluten-free" in dietary_restrictions:
                        carb_examples = ["Brown rice", "Sweet potato", "Quinoa", "Gluten-free oats"]
                    
                    # Column layout for examples
                    for i, veg in enumerate(veg_examples[:5]):
                        ax.text(0.15, 0.65 - i*0.06, f"• {veg}", fontsize=9, color='#1b5e20')
                    
                    for i, protein in enumerate(protein_examples):
                        ax.text(0.52, 0.85 - i*0.05, f"• {protein}", fontsize=7, color='#e65100')
                    
                    for i, carb in enumerate(carb_examples[:4]):
                        ax.text(0.52, 0.45 - i*0.06, f"• {carb}", fontsize=9, color='#0d47a1')
                    
                    # Add a helpful title with personalization
                    title = "Diabetes-Friendly Portion Guide"
                    if cultural_preferences:
                        title = f"Diabetes-Friendly Portion Guide ({cultural_preferences} Focus)"
                    
                    ax.text(0.5, 0.95, title, ha='center', va='center', 
                            fontsize=16, fontweight='bold', color='#333333')
                    
                    # Add a footnote
                    ax.text(0.5, 0.05, "For optimal blood sugar management, follow this portion guide", 
                            ha='center', va='center', fontsize=10, color='#555555', style='italic')
                    
                    # Set limits and remove axes
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    ax.axis('off')
                    
                    return fig
                except Exception as e:
                    st.error(f"Error creating enhanced portion guide: {e}")
                    return None
            
            # Display the enhanced portion guide
            portion_guide = create_enhanced_portion_guide()
            if portion_guide is not None:
                st.pyplot(portion_guide)
            
            # Add educational note about the portion guide with personalization
            portion_guide_html = """
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
                <h4 style="color: #2e7d32;">How to Use This Portion Guide</h4>
                <ul>
                    <li><strong>Half your plate</strong> should be filled with non-starchy vegetables</li>
                    <li><strong>One quarter</strong> should contain lean proteins</li>
                    <li><strong>One quarter</strong> should have complex carbohydrates</li>
                    <li>Include a small serving of fruit and/or dairy on the side</li>
                    <li>Add healthy fats in small amounts (olive oil, avocado, nuts)</li>
            """

            
            st.markdown(portion_guide_html, unsafe_allow_html=True)
            
            # Add a separator
            st.markdown("---")
            
            # Add the blood glucose target range visualization
            def create_enhanced_glucose_guide():
                try:
                    from matplotlib.patches import Rectangle, Polygon
                    import numpy as np
                    
                    fig, ax = plt.subplots(figsize=(10, 4), facecolor='#f8f9fa')
                    ax.set_facecolor('#f8f9fa')
                    
                    # Create a more attractive glucose meter visualization
                    # Low range (red)
                    ax.add_patch(Rectangle((0, 0.2), 0.3, 0.6, color='#ffcdd2', alpha=0.7))
                    ax.text(0.15, 0.5, "LOW\n< 70 mg/dL\n\nSymptoms:\nShaking, sweating,\nconfusion, dizziness", 
                            ha='center', va='center', fontsize=10, color='#c62828')
                    
                    # Target range (green)
                    ax.add_patch(Rectangle((0.3, 0.2), 0.4, 0.6, color='#c8e6c9', alpha=0.7))
                    ax.text(0.5, 0.5, "TARGET RANGE\n70-180 mg/dL\n\nGoal:\nStay in this range\nas much as possible", 
                            ha='center', va='center', fontsize=12, fontweight='bold', color='#2e7d32')
                    
                    # High range (red)
                    ax.add_patch(Rectangle((0.7, 0.2), 0.3, 0.6, color='#ffcdd2', alpha=0.7))
                    ax.text(0.85, 0.5, "HIGH\n> 180 mg/dL\n\nSymptoms:\nThirst, fatigue,\nfrequent urination", 
                            ha='center', va='center', fontsize=10, color='#c62828')
                    
                    # Add a meter-like pointer
                    triangle_vertices = np.array([[0.5, 0.2], [0.47, 0.15], [0.53, 0.15]])
                    meter = Polygon(triangle_vertices, color='#333333')
                    ax.add_patch(meter)
                    
                    # Add a title
                    ax.text(0.5, 0.9, "BLOOD GLUCOSE TARGET RANGES", ha='center', va='center', 
                            fontsize=16, fontweight='bold', color='#333333')
                    
                    # Set limits and remove axes
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    ax.axis('off')
                    
                    return fig
                except Exception as e:
                    st.error(f"Error creating enhanced glucose guide: {e}")
                    return None
            
            # Display the enhanced glucose guide
            glucose_guide = create_enhanced_glucose_guide()
            if glucose_guide is not None:
                st.pyplot(glucose_guide)
            
            # Add a separator
            st.markdown("---")

            # Create foods to avoid visual based on preferences
            def create_foods_to_avoid_visual():
                try:
                    # Create figure with a clean white background and optimized dimensions
                    fig, ax = plt.subplots(figsize=(7, 3))
                    
                    # Set figure background color and reduce margins
                    fig.patch.set_facecolor('#f8f9fa')
                    ax.set_facecolor('#f8f9fa')
                    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.1)
                    
                    # Add title - reduced font size
                    ax.text(0.5, 0.88, "Foods to Limit or Avoid with Diabetes", 
                            ha='center', fontsize=13, fontweight='bold', color='#d32f2f')
                    
                    # Define foods to avoid - customize based on user preferences
                    foods = [
                        "Sugary Drinks", 
                        "White Bread", 
                        "Fried Foods",
                        "Processed Meats", 
                        "Sweets & Desserts"
                    ]
                    
                    # Customize based on dietary restrictions
                    if dietary_restrictions:
                        if "Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions:
                            foods[3] = "Processed Foods"  # Replace "Processed Meats" for vegetarians/vegans
                    
                    # Create more compact positions for items (in a single row)
                    num_items = len(foods)
                    x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
                    y_position = 0.55  # Center position
                    
                    # Draw each food item with prohibition symbol - smaller size
                    for i, (x, food) in enumerate(zip(x_positions, foods)):
                        # Draw red circle - smaller size
                        circle = plt.Circle((x, y_position), 0.05, fill=False, 
                                        edgecolor='red', linewidth=1.5)
                        ax.add_patch(circle)
                        
                        # Draw diagonal line for "no" symbol - smaller
                        ax.plot([x-0.035, x+0.035], [y_position+0.035, y_position-0.035], 
                            color='red', linewidth=1.5)
                        
                        # Add food label - smaller font
                        ax.text(x, y_position-0.1, food, ha='center', fontsize=8, 
                            fontweight='bold')
                    
                    # More compact explanation at bottom
                    ax.text(0.5, 0.22, "These foods can cause rapid blood sugar spikes and worsen insulin resistance", 
                        ha='center', fontsize=9, fontstyle='italic')
                    
                    # Set limits and remove axes
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    ax.axis('off')
                    
                    # Tight layout to reduce whitespace
                    plt.tight_layout()
                    
                    return fig
                except Exception as e:
                    st.error(f"Error creating foods to avoid visual: {e}")
                    return None

            # Display the foods to avoid visual
            foods_to_avoid = create_foods_to_avoid_visual()
            if foods_to_avoid is not None:
                st.pyplot(foods_to_avoid)

            # Create a container for the "Foods to Limit" section
            limit_container = st.container()

            with limit_container:
                # Add a custom header with red background using markdown and CSS
                st.markdown(
                    """
                    <div style="background-color: #ffebee; padding: 15px; border-radius: 10px;">
                        <h4 style="color: #c62828; margin-top: 0;">Why Limit These Foods?</h4>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Create a list of foods to limit with icons and explanations
                limit_foods = [
                    {"icon": "🍞", "name": "White Bread and Refined Grains", "reason": "Cause rapid blood sugar spikes"},
                    {"icon": "🥤", "name": "Sugary Drinks", "reason": "High in simple sugars with little nutritional value"},
                    {"icon": "🍟", "name": "Fried Foods", "reason": "High in unhealthy fats that can worsen insulin resistance"}
                ]
                
                # Add conditional item based on dietary restrictions
                if dietary_restrictions and ("Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions):
                    limit_foods.append({"icon": "🥫", "name": "Processed Foods", "reason": "Often high in sodium, sugar, and unhealthy additives"})
                else:
                    limit_foods.append({"icon": "🥓", "name": "Processed Meats", "reason": "High in sodium and unhealthy fats"})
                
                limit_foods.append({"icon": "🍰", "name": "Sweets & Desserts", "reason": "High in sugar and calories with minimal nutrition"})
                
                # Display each food item
                for food in limit_foods:
                    cols = st.columns([1, 5])
                    with cols[0]:
                        st.markdown(f"<span style='font-size: 36px;'>{food['icon']}</span>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"**{food['name']}**: {food['reason']}")
                
                # Add a bottom padding
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


            # Add a separator
            st.markdown("---")

            # Create recommended foods visual based on preferences
            def create_recommended_foods_visual():
                try:
                    # Create figure with a tight layout and adjusted dimensions
                    # Make the figure wider and shorter to fit horizontally on the page
                    fig, ax = plt.subplots(figsize=(7, 3))
                    
                    # Set figure background color and reduce margins
                    fig.patch.set_facecolor('#f8f9fa')
                    ax.set_facecolor('#f8f9fa')
                    plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.1)
                    
                    # Add title with reduced font size
                    title = "Recommended Foods for Blood Sugar Management"
                    if cultural_preferences:
                        title = f"Recommended Foods ({cultural_preferences} Options)"
                    
                    ax.text(0.5, 0.88, title, 
                            ha='center', fontsize=13, fontweight='bold', color='#2e7d32')
                    
                    # Define recommended foods - customize based on user preferences
                    foods = [
                        "Whole Grains", 
                        "Fresh Fruit", 
                        "Protein",
                        "Healthy Fats", 
                        "Legumes"
                    ]
                    
                    # Customize based on dietary or cultural preferences
                    if dietary_restrictions:
                        if "vegetarian" in dietary_restrictions:
                            foods[2] = "Plant Protein"
                        elif "vegan" in dietary_restrictions:
                            foods[2] = "Plant Protein"
                    
                    # Create more compact positions for items (in a single row)
                    num_items = len(foods)
                    x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
                    y_position = 0.55  # Center position
                    
                    # Draw each food item with checkmark - smaller size
                    for i, (x, food) in enumerate(zip(x_positions, foods)):
                        # Draw green circle - smaller size
                        circle = plt.Circle((x, y_position), 0.05, fill=True, 
                                        facecolor='#c8e6c9', edgecolor='#2e7d32', linewidth=1.5)
                        ax.add_patch(circle)
                        
                        # Draw checkmark - smaller
                        ax.plot([x-0.025, x-0.008, x+0.03], [y_position-0.008, y_position-0.025, y_position+0.025], 
                            color='#2e7d32', linewidth=1.5)
                        
                        # Add food label - smaller font
                        ax.text(x, y_position-0.1, food, ha='center', fontsize=8, 
                            fontweight='bold')
                    
                    # More compact explanation at bottom
                    # Simple one-line message instead of multiple bullets
                    ax.text(0.5, 0.22, "These foods help maintain steady blood glucose levels and support overall health", 
                        ha='center', fontsize=9, fontstyle='italic')
                    
                    # Set limits and remove axes
                    ax.set_xlim(0, 1)
                    ax.set_ylim(0, 1)
                    ax.axis('off')
                    
                    # Tight layout to reduce whitespace
                    plt.tight_layout()
                    
                    return fig
                except Exception as e:
                    st.error(f"Error creating recommended foods visual: {e}")
                    return None

            # Display the recommended foods visual
            recommended_foods = create_recommended_foods_visual()
            if recommended_foods is not None:
                st.pyplot(recommended_foods)

            # Customize "Why Choose These Foods?" explanation based on preferences
            # Create a container for the "Foods to Choose" section
            choose_container = st.container()

            with choose_container:
                # Add a custom header with green background using markdown and CSS
                st.markdown(
                    """
                    <div style="background-color: #e8f5e9; padding: 0px; border-radius: 0px;">
                        <h4 style="color: #2e7d32; margin-top: 10;">Why Choose These Foods?</h4>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Create a list of recommended foods with icons and explanations
                choose_foods = [
                    {"icon": "🌾", "name": "Whole Grains", "reason": "High in fiber which slows sugar absorption into the bloodstream"},
                    {"icon": "🍎", "name": "Fresh Fruit", "reason": "Contains natural sugars with fiber, vitamins, and antioxidants"}
                ]
                
                # Customize protein examples based on dietary preferences
                if dietary_restrictions and "Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions:
                    choose_foods.append({"icon": "🥚", "name": "Protein", "reason": "Options like tofu, legumes, and eggs provide protein without raising blood sugar"})
                else:
                    choose_foods.append({"icon": "🍗", "name": "Protein", "reason": "Helps maintain steady blood sugar and promotes satiety"})
                
                # Customize fat examples based on cultural preferences
                if cultural_preferences and "Mediterranean" in cultural_preferences:
                    choose_foods.append({"icon": "🫒", "name": "Olive Oil", "reason": "Mediterranean staple that improves insulin sensitivity"})
                else:
                    choose_foods.append({"icon": "🥑", "name": "Healthy Fats", "reason": "Improves insulin sensitivity and slows digestion of carbohydrates"})
                
                # Customize legumes example based on cultural preferences
                if cultural_preferences and "Latin" in cultural_preferences:
                    choose_foods.append({"icon": "🫘", "name": "Beans", "reason": "Latin American staple high in protein and fiber with minimal impact on blood glucose"})
                else:
                    choose_foods.append({"icon": "🫘", "name": "Legumes", "reason": "High in protein and fiber with minimal impact on blood glucose"})
                
                # Display each food item
                for food in choose_foods:
                    cols = st.columns([1, 5])
                    with cols[0]:
                        st.markdown(f"<span style='font-size: 36px;'>{food['icon']}</span>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"**{food['name']}**: {food['reason']}")
                
                # Add a bottom padding
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        else:
            st.warning("No visual guidance has been generated yet.")
    
    # Add download button and adjustment button
    # col1, col2 = st.columns([1, 2])
    
    # with col1:
    #     st.download_button(
    #         label="⬇️ Download PDF",
    #         data="This would be a generated PDF in a production environment",  # In production this would be the PDF
    #         file_name="diabetes_nutrition_plan.pdf",
    #         mime="application/pdf",
    #         use_container_width=True,
    #         key="download_plan_pdf"  # Add this unique key
    #    )
    #with col2:
        # Add button to return to input data
    #    if st.button("🔄 Make Adjustments to Your Plan", 
    #                use_container_width=True,
    #                key="adjust_plan_button"):  # Add this unique key
    #        st.session_state.nav_to_input = True
    #        st.rerun()

def create_recommended_foods_visual():
    try:
        # Create figure with a clean white background and tight dimensions
        fig, ax = plt.subplots(figsize=(8, 3.5))
        
        # Add title
        ax.text(0.5, 0.85, "Recommended Foods for Blood Sugar Management", 
                ha='center', fontsize=14, fontweight='bold', color='#2e7d32')
        
        # Define recommended foods
        foods = [
            "Whole Grains", 
            "Fresh Fruit", 
            "Lean Protein",
            "Healthy Fats", 
            "Legumes"
        ]
        
        # Create positions for items (in a single row)
        num_items = len(foods)
        x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
        y_position = 0.55
        
        # Draw each food item with checkmark
        for i, (x, food) in enumerate(zip(x_positions, foods)):
            # Draw green circle
            circle = plt.Circle((x, y_position), 0.06, fill=True, 
                              facecolor='#c8e6c9', edgecolor='#2e7d32', linewidth=1.5)
            ax.add_patch(circle)
            
            # Draw checkmark
            ax.plot([x-0.03, x-0.01, x+0.035], [y_position-0.01, y_position-0.03, y_position+0.03], 
                   color='#2e7d32', linewidth=2)
            
            # Add food label
            ax.text(x, y_position-0.12, food, ha='center', fontsize=10, 
                   fontweight='bold')
        
        # Add explanation at bottom
        ax.text(0.5, 0.25, "These foods help stabilize blood sugar levels", 
               ha='center', fontsize=11)
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Tight layout to reduce whitespace
        plt.tight_layout()
        
        return fig
    except Exception as e:
        st.error(f"Error creating recommended foods visual: {e}")
        return None
    
def create_foods_to_avoid_visual():
    try:
        # Create figure with a clean white background and tighter dimensions
        fig, ax = plt.subplots(figsize=(8, 3.5))
        
        # Add title
        ax.text(0.5, 0.85, "Foods to Limit or Avoid with Diabetes", 
                ha='center', fontsize=14, fontweight='bold', color='#d32f2f')
        
        # Define foods to avoid
        foods = [
            "Sugary Drinks", 
            "White Bread", 
            "Fried Foods",
            "Processed Meats", 
            "Sweets & Desserts"
        ]
        
        # Create positions for items (in a single row)
        num_items = len(foods)
        x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
        y_position = 0.55  # Moved up for more compact layout
        
        # Draw each food item with prohibition symbol
        for i, (x, food) in enumerate(zip(x_positions, foods)):
            # Draw red circle
            circle = plt.Circle((x, y_position), 0.06, fill=False, 
                               edgecolor='red', linewidth=2)
            ax.add_patch(circle)
            
            # Draw diagonal line for "no" symbol
            ax.plot([x-0.045, x+0.045], [y_position+0.045, y_position-0.045], 
                   color='red', linewidth=2)
            
            # Add food label (smaller text)
            ax.text(x, y_position-0.12, food, ha='center', fontsize=10, 
                   fontweight='bold')
                
        ax.text(0.5, 0.25, "These foods can cause rapid blood sugar spikes", 
               ha='center', fontsize=11)
               
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Tight layout to reduce whitespace
        plt.tight_layout()
        
        return fig
    except Exception as e:
        st.error(f"Error creating foods to avoid visual: {e}")
        return None

def show_educational_resources():
    """Display educational resources about diabetes nutrition."""
    st.header("Educational Resources")
    
    # Create tabs
    tab_names = [
        "Diabetes Basics", 
        "Food & Nutrition", 
        "Physical Activity", 
        "Monitoring", 
        "Cultural Adaptations"
    ]
    
    tabs = st.tabs(tab_names)
    
    st.markdown("---")
    
    # Use with blocks for each tab instead of conditional statements
    with tabs[0]:  # Diabetes Basics tab
        st.subheader("Understanding Diabetes")
        
        st.markdown("""
        #### What is Diabetes?
        Diabetes is a chronic condition that affects how your body turns food into energy. There are several types:
        
        - **Type 1 Diabetes**: The body doesn't produce insulin. This is usually diagnosed in children and young adults.
        - **Type 2 Diabetes**: The body doesn't use insulin properly. This is the most common type.
        - **Gestational Diabetes**: Develops during pregnancy in women who don't already have diabetes.
        - **Prediabetes**: Blood sugar is higher than normal but not high enough to be diagnosed as type 2 diabetes.
        
        #### How Diabetes Affects Your Body
        When you eat, your body turns food into glucose (sugar) that enters your bloodstream. Your pancreas releases insulin to help move glucose from the blood into cells for energy. With diabetes, either your body doesn't make enough insulin or can't use it effectively, leading to high blood sugar levels.
        
        #### Importance of Blood Sugar Management
        Consistently high blood sugar can damage your blood vessels and nerves over time, leading to complications like:
        - Heart disease
        - Kidney disease
        - Vision problems
        - Nerve damage
        - Foot problems
        
        Managing your blood sugar through diet, exercise, medication (if prescribed), and regular monitoring is essential for long-term health.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Blood Sugar Targets
            General targets for blood sugar levels:
            - **Before meals**: 80-130 mg/dL
            - **2 hours after meals**: Less than 180 mg/dL
            - **HbA1c**: Less than 7%
            
            Your healthcare provider may set different targets based on your individual situation.
            """)
        
        with col2:
            # Sample blood glucose chart
            def create_glucose_chart():
                fig, ax = plt.subplots(figsize=(6, 4))
                
                # Sample data
                times = ["Fasting", "Before Lunch", "Before Dinner", "Bedtime"]
                target_min = [80, 80, 80, 100]
                target_max = [130, 130, 130, 140]
                
                # Plot target ranges
                for i in range(len(times)):
                    ax.plot([i, i], [target_min[i], target_max[i]], 'g', linewidth=10, alpha=0.5)
                
                ax.set_xticks(range(len(times)))
                ax.set_xticklabels(times)
                ax.set_ylabel("Blood Glucose (mg/dL)")
                ax.set_title("Target Blood Glucose Ranges")
                ax.grid(True, linestyle='--', alpha=0.7)
                
                return fig
            
            st.pyplot(create_glucose_chart())
    
    with tabs[1]:  # Food & Nutrition tab
        st.subheader("Nutrition for Diabetes Management")
        
        # Rest of the Food & Nutrition content...
        # Existing code for this section
        
        st.markdown("""
        #### Key Principles of Diabetes Nutrition
        
        1. **Carbohydrate Management**: Carbohydrates have the most impact on blood sugar. Focus on:
           - Consistent carb intake at meals
           - Choosing complex carbs over simple sugars
           - Learning about portion sizes
        
        2. **Balanced Meals**: Include:
           - Healthy carbohydrates (whole grains, fruits, vegetables, legumes)
           - Lean proteins (fish, chicken, beans, tofu)
           - Healthy fats (olive oil, nuts, avocados)
           - Plenty of fiber
        
        3. **Plate Method**: A simple way to build balanced meals
           - ½ plate: non-starchy vegetables
           - ¼ plate: lean protein
           - ¼ plate: carbohydrates
           - Small amount of healthy fat
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Glycemic Index and Load
            The **Glycemic Index (GI)** measures how quickly foods raise blood sugar:
            - **Low GI (55 or less)**: Oatmeal, sweet potatoes, most fruits
            - **Medium GI (56-69)**: Brown rice, whole wheat bread
            - **High GI (70+)**: White bread, white rice, potatoes
            
            **Glycemic Load** considers both the GI and the amount of carbs in a serving, giving a more practical measure of a food's impact on blood sugar.
            """)
        
        with col2:
            # Sample plate method visual
            def create_plate_method():
                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
                
                # Data for the pie chart
                data = [50, 25, 25]
                labels = ['Non-starchy Vegetables', 'Protein', 'Carbohydrates']
                colors = ['#4CAF50', '#FFC107', '#2196F3']
                
                # Create the pie chart
                wedges, texts, autotexts = ax.pie(
                    data, 
                    labels=labels, 
                    colors=colors,
                    autopct='%1.0f%%',
                    startangle=90,
                    wedgeprops={'edgecolor': 'w', 'linewidth': 2}
                )
                
                ax.set_title('Diabetes Plate Method', fontsize=16)
                
                return fig
            
            st.pyplot(create_plate_method())
    
    with tabs[2]:  # Physical Activity tab
        st.subheader("Physical Activity and Diabetes")
        
        # Rest of the Physical Activity content...
        # Existing code for this section
        
        st.markdown("""
        #### Benefits of Physical Activity for Diabetes
        
        Regular physical activity:
        - Lowers blood glucose by increasing insulin sensitivity
        - Helps maintain a healthy weight
        - Reduces cardiovascular disease risk
        - Improves mood and reduces stress
        - Strengthens muscles and bones
        
        #### Recommended Activity
        
        - **Aim for 150 minutes of moderate-intensity activity per week**
        - Spread activity throughout the week (e.g., 30 minutes, 5 days a week)
        - Include both aerobic exercise and strength training
        - Start slowly and gradually increase intensity
        
        #### Types of Physical Activity
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Aerobic Exercise**
            - Walking
            - Swimming
            - Cycling
            - Dancing
            
            **Strength Training**
            - Weight lifting
            - Resistance bands
            - Bodyweight exercises
            
            **Flexibility & Balance**
            - Yoga
            - Stretching
            - Tai Chi
            """)
        
        with col2:
            # Sample activity benefits chart
            def create_activity_chart():
                fig, ax = plt.subplots(figsize=(6, 5))
                
                activities = ["Walking", "Swimming", "Cycling", "Strength Training", "Yoga"]
                minutes = [30, 30, 30, 20, 20]
                
                # Create horizontal bars
                ax.barh(activities, minutes, color='#42A5F5')
                
                ax.set_xlabel("Recommended Minutes per Session")
                ax.set_title("Recommended Activities for Diabetes")
                ax.grid(True, linestyle='--', alpha=0.7, axis='x')
                
                return fig
            
            st.pyplot(create_activity_chart())
        
        st.markdown("""
        #### Safety Tips
        
        - Check blood glucose before, during (for long sessions), and after activity
        - Carry fast-acting carbs (like glucose tablets) in case of low blood sugar
        - Stay hydrated
        - Wear proper footwear and inspect feet after activity
        - Start with low intensity and gradually increase
        - Talk to your healthcare provider before starting a new exercise program
        """)
    
    with tabs[3]:  # Monitoring tab
        st.subheader("Monitoring Blood Glucose")
        
        # Rest of the Monitoring content...
        # Existing code for this section
        
        st.markdown("""
        #### Why Monitor Blood Glucose?
        
        Regular monitoring helps you:
        - Understand how food, activity, medication, and stress affect your blood sugar
        - Detect patterns and make adjustments to your management plan
        - Prevent or address high and low blood sugar episodes
        - Track your progress toward goals
        - Make informed decisions about food, activity, and medication
        
        #### When to Check Blood Glucose
        
        Common times to check include:
        - First thing in the morning (fasting)
        - Before meals
        - 1-2 hours after meals
        - Before and after physical activity
        - Before driving
        - When you feel symptoms of high or low blood sugar
        
        Your healthcare provider will recommend a specific schedule based on your needs.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Understanding Your Results
            
            General target ranges (may vary based on provider recommendations):
            
            - **Before meals**: 80-130 mg/dL
            - **1-2 hours after meals**: Less than 180 mg/dL
            - **Bedtime**: 100-140 mg/dL
            
            **HbA1c**: Measures average blood sugar over 2-3 months
            - Target for most adults with diabetes: Less than 7%
            
            #### Responding to Results
            
            **High Blood Sugar (Hyperglycemia)**
            - Drink water
            - Take medication as prescribed
            - Physical activity (if blood sugar isn't extremely high)
            - Check for illness or stress
            
            **Low Blood Sugar (Hypoglycemia)**
            - Follow the 15-15 Rule: Consume 15g of fast-acting carbs, wait 15 minutes, recheck
            - Examples of 15g carbs: 4 glucose tablets, 4 oz juice, 1 tbsp honey
            """)
        
        with col2:
            # Sample blood glucose log
            def create_glucose_log():
                fig, ax = plt.subplots(figsize=(6, 5))
                
                # Sample data
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                fasting = [95, 102, 88, 110, 92]
                after_breakfast = [145, 160, 135, 172, 148]
                after_lunch = [138, 152, 140, 165, 130]
                after_dinner = [150, 145, 135, 180, 142]
                
                ax.plot(days, fasting, 'o-', label='Fasting')
                ax.plot(days, after_breakfast, 's-', label='After Breakfast')
                ax.plot(days, after_lunch, '^-', label='After Lunch')
                ax.plot(days, after_dinner, 'd-', label='After Dinner')
                
                # Add target range
                ax.axhspan(80, 130, alpha=0.2, color='green', label='Target Before Meals')
                ax.axhspan(130, 180, alpha=0.2, color='yellow', label='Target After Meals')
                
                ax.set_ylabel('Blood Glucose (mg/dL)')
                ax.set_title('Sample Blood Glucose Log')
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.legend()
                
                fig.autofmt_xdate()  # Rotate x-labels for better fit
                
                return fig
            
            st.pyplot(create_glucose_log())
    
    with tabs[4]:  # Cultural Adaptations tab
        
        st.markdown("""#### Cultural Adaptations for Diabetes Management""")
        # Rest of the Cultural Adaptations content...
        # Existing code for this section
        
        region = st.selectbox(
            "Select a Region for Cultural Adaptations",
            ["African Cuisine", "South Asian Cuisine", "Latin American Cuisine", "Middle Eastern Cuisine", "East Asian Cuisine"]
        )
        
        if region == "African Cuisine":
            st.markdown("""
            #### Adapting African Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Leafy greens (amaranth, collard greens, kale)
            - Legumes (black-eyed peas, chickpeas, lentils)
            - Lean proteins (fish, chicken, game meats)
            - Whole grains (millet, sorghum, brown rice)
            - Healthy fats (peanuts, avocados)
            
            **Modified Preparation Methods:**
            - Reduce palm oil and coconut oil; increase use of olive or peanut oil
            - Use less salt and bouillon cubes; flavor with herbs and spices
            - Bake, grill, or stew instead of deep frying
            - Cook starches until slightly firm ("al dente") to lower glycemic impact
            
            **Traditional Dishes - Healthier Versions:**
            - Jollof Rice: Use brown rice, increase vegetables, reduce oil
            - Fufu/Pounded Yam: Smaller portions, pair with vegetable soup
            - Stews: Increase vegetables, reduce oil, choose lean meats
            """)
        
        elif region == "South Asian Cuisine":
            st.markdown("""
            #### Adapting South Asian Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Legumes (lentils, chickpeas, beans)
            - Non-starchy vegetables (bitter gourd, okra, eggplant)
            - Lean proteins (fish, chicken, tofu)
            - Whole grains (brown rice, barley, millet)
            - Healthy fats (mustard oil, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Reduce ghee and coconut oil; use mustard oil or olive oil in moderation
            - Bake, grill, or steam instead of frying
            - Use less rice and more vegetables and proteins
            - Incorporate more bitter gourd, fenugreek, and cinnamon (help with glucose control)
            
            **Traditional Dishes - Healthier Versions:**
            - Dal: Emphasize this high-fiber, protein-rich dish
            - Chapati: Use whole wheat flour, make thinner
            - Curry: Increase vegetables, reduce oil, use low-fat yogurt instead of cream
            - Rice: Mix cauliflower rice with regular rice to reduce carbs
            """)
        
        elif region == "Latin American Cuisine":
            st.markdown("""
            #### Adapting Latin American Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Beans and legumes (black beans, pinto beans, lentils)
            - Vegetables (nopales, chayote, tomatoes, peppers)
            - Lean proteins (fish, chicken, lean cuts of beef)
            - Whole grains (brown rice, corn tortillas in moderation)
            - Healthy fats (avocados, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Use less lard and more olive oil or avocado oil
            - Bake, grill, or steam instead of frying
            - Use fresh ingredients rather than processed foods
            - Season with herbs and spices instead of salt
            
            **Traditional Dishes - Healthier Versions:**
            - Tacos: Use corn tortillas (smaller), increase vegetables, choose lean proteins
            - Rice: Mix cauliflower rice with regular rice, add vegetables
            - Beans: Keep these high-fiber foods, but prepare with less fat
            - Nopales (cactus): Emphasize this low-glycemic vegetable
            """)
        
        elif region == "Middle Eastern Cuisine":
            st.markdown("""
            #### Adapting Middle Eastern Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Legumes (chickpeas, lentils, fava beans)
            - Vegetables (eggplant, peppers, tomatoes, greens)
            - Lean proteins (fish, chicken, lean lamb)
            - Whole grains (bulgur, freekeh, whole wheat pita in moderation)
            - Healthy fats (olive oil, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Use olive oil in moderation
            - Bake, grill, or roast instead of frying
            - Season with herbs and spices instead of salt
            - Reduce honey and sugar in recipes
            
            **Traditional Dishes - Healthier Versions:**
            - Hummus: High in fiber and protein, moderate portions
            - Tabbouleh: Emphasize this parsley-rich salad
            - Shawarma: Use lean meats, whole wheat wrap, plenty of vegetables
            - Stuffed vegetables: Include more lean protein, reduce rice
            """)
        
        elif region == "East Asian Cuisine":
            st.markdown("""
            #### Adapting East Asian Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Vegetables (bok choy, Chinese broccoli, mushrooms, seaweed)
            - Lean proteins (fish, tofu, chicken)
            - Legumes (edamame, tofu)
            - Whole grains (brown rice in moderation)
            - Healthy fats (sesame oil in moderation, nuts)
            
            **Modified Preparation Methods:**
            - Steam, stir-fry, or boil instead of deep frying
            - Use less oil in cooking
            - Reduce sodium (soy sauce, MSG)
            - Choose brown rice over white rice
            
            **Traditional Dishes - Healthier Versions:**
            - Stir-fries: Increase vegetable-to-meat ratio, use less oil
            - Rice: Mix cauliflower rice with regular rice, smaller portions
            - Soups: Clear broths with vegetables and lean proteins
            - Steam dishes: Emphasize steamed fish and vegetables
            """)
        
        st.markdown("""
        #### General Principles for Cultural Adaptation
        
        1. **Preserve Cultural Identity**: Modify traditional dishes rather than eliminate them
        2. **Use Traditional Wisdom**: Many cultures have traditional foods that are beneficial for diabetes
        3. **Focus on Cooking Methods**: Often changing preparation method is easier than changing the food itself
        4. **Portion Control**: Sometimes enjoying smaller amounts of traditional foods is the best approach
        5. **Community Involvement**: Include family and community in dietary changes for better support
        """)


def create_risk_dashboard(health_data):
    """Create a comprehensive risk assessment dashboard visualization."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
    import matplotlib.patheffects as path_effects
    import numpy as np
    
    # Extract health metrics
    age = health_data.get('age', 45)
    gender = health_data.get('gender', 'Unknown')
    bmi = health_data.get('bmi', 25)
    fasting_glucose = health_data.get('fasting_glucose', 100)
    hba1c = health_data.get('hba1c', 5.7)
    activity_level = health_data.get('activity_level', 'Moderately Active')
    
    # Map activity level to a numeric score (1-5)
    activity_scores = {
        'Sedentary': 1,
        'Lightly Active': 2,
        'Moderately Active': 3,
        'Very Active': 4,
        'Extra Active': 5
    }
    activity_score = activity_scores.get(activity_level, 3)
    
    # Calculate risk scores (simplified algorithm)
    # Each score ranges from 0-10, where 0 is lowest risk and 10 is highest
    
    # Glucose Risk (based on fasting glucose and HbA1c)
    glucose_risk = 0
    if fasting_glucose < 100 and hba1c < 5.7:
        glucose_risk = 0  # Optimal
    elif fasting_glucose < 100 and hba1c < 6.0:
        glucose_risk = 2  # Normal but slightly elevated HbA1c
    elif fasting_glucose < 110 and hba1c < 6.0:
        glucose_risk = 3  # Slightly elevated
    elif fasting_glucose < 126 and hba1c < 6.5:
        glucose_risk = 5  # Prediabetes range
    elif fasting_glucose < 140 and hba1c < 7.0:
        glucose_risk = 7  # Early diabetes range
    elif fasting_glucose < 180 and hba1c < 8.0:
        glucose_risk = 8  # Diabetes with moderate control
    else:
        glucose_risk = 10  # Diabetes with poor control
    
    # BMI Risk
    bmi_risk = 0
    if bmi < 18.5:
        bmi_risk = 3  # Underweight
    elif 18.5 <= bmi < 25:
        bmi_risk = 0  # Normal
    elif 25 <= bmi < 30:
        bmi_risk = 3  # Overweight
    elif 30 <= bmi < 35:
        bmi_risk = 6  # Obese Class I
    elif 35 <= bmi < 40:
        bmi_risk = 8  # Obese Class II
    else:
        bmi_risk = 10  # Obese Class III
    
    # Activity Risk (inversely related to activity level)
    activity_risk = max(0, 10 - activity_score * 2)
    
    # Age Risk (simplified, increases with age)
    age_risk = min(10, max(0, (age - 30) / 5))
    
    # Cardiovascular Risk (simplified combination of other risks)
    cv_risk = (glucose_risk * 0.3 + bmi_risk * 0.3 + activity_risk * 0.2 + age_risk * 0.2)
    
    # Overall Health Risk (average of all risks)
    overall_risk = (glucose_risk + bmi_risk + activity_risk + age_risk) / 4
    
    # Create figure with modern style
    plt.style.use('ggplot')
    fig, axs = plt.subplots(2, 3, figsize=(15, 10), facecolor='#f8f9fa')
    fig.suptitle('Health Risk Assessment Dashboard', fontsize=24, y=0.98, 
               fontweight='bold', color='#2c3e50')
    
    # Flatten axs for easier iteration
    axs = axs.flatten()
    
    # Set background color for all axes
    for ax in axs:
        ax.set_facecolor('#f8f9fa')
    
    # Function to create a risk gauge
    def create_risk_gauge(ax, risk_score, title, color_scheme='default'):
        ax.clear()
        
        # Define color schemes
        if color_scheme == 'default':
            colors = ['#2ecc71', '#f1c40f', '#e74c3c']  # Green, Yellow, Red
        elif color_scheme == 'glucose':
            colors = ['#2ecc71', '#f1c40f', '#e74c3c']  # Green, Yellow, Red
        elif color_scheme == 'cv':
            colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red
        elif color_scheme == 'activity':
            colors = ['#3498db', '#2ecc71', '#f1c40f']  # Blue, Green, Yellow
        else:
            colors = ['#2ecc71', '#f1c40f', '#e74c3c']  # Default
        
        # Calculate color based on risk score
        if risk_score < 3.33:
            color = colors[0]  # Low risk
            risk_category = "Low Risk"
        elif risk_score < 6.66:
            color = colors[1]  # Medium risk
            risk_category = "Moderate Risk"
        else:
            color = colors[2]  # High risk
            risk_category = "High Risk"
        
        # Add a fancy background
        background = FancyBboxPatch((0.1, 0.1), 0.8, 0.8, boxstyle="round,pad=0.02", 
                                  fc='white', ec='#bdc3c7', lw=1, alpha=0.7, zorder=0)
        background.set_path_effects([path_effects.SimplePatchShadow(), path_effects.Normal()])
        ax.add_patch(background)
        
        # Draw a circular gauge
        center = (0.5, 0.45)
        radius = 0.3
        
        # Background circle (gray)
        bg_circle = Circle(center, radius, fc='#ecf0f1', ec='#bdc3c7', lw=2, alpha=0.8, zorder=1)
        ax.add_patch(bg_circle)
        
        # Calculate angle based on risk score (0-10 maps to 240° to -60°)
        angle = np.radians(240 - risk_score * 30)
        
        # Draw filled arc representing risk level
        theta1 = np.radians(240)
        theta2 = angle
        
        # Generate points for filled arc
        n_points = 50
        theta = np.linspace(theta1, theta2, n_points)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        
        # Add center point to create a filled pie slice
        points = np.column_stack([x, y])
        points = np.vstack([points, [center[0], center[1]]])
        
        # Create filled arc
        ax.fill(points[:, 0], points[:, 1], color=color, alpha=0.8, zorder=2)
        
        # Add tick marks and labels
        for i, tick in enumerate(np.linspace(0, 10, 6)):
            tick_angle = np.radians(240 - tick * 30)
            # Outer tick position
            x_outer = center[0] + (radius + 0.02) * np.cos(tick_angle)
            y_outer = center[1] + (radius + 0.02) * np.sin(tick_angle)
            # Inner tick position
            x_inner = center[0] + (radius - 0.02) * np.cos(tick_angle)
            y_inner = center[1] + (radius - 0.02) * np.sin(tick_angle)
            
            # Draw tick line
            ax.plot([x_inner, x_outer], [y_inner, y_outer], 'k-', lw=1, alpha=0.5, zorder=3)
            
            # Add label for even ticks
            if i % 2 == 0:
                x_label = center[0] + (radius + 0.06) * np.cos(tick_angle)
                y_label = center[1] + (radius + 0.06) * np.sin(tick_angle)
                ax.text(x_label, y_label, f"{int(tick)}", ha='center', va='center', 
                       fontsize=8, color='#7f8c8d', zorder=3)
        
        # Add categories
        category_positions = [(0.25, 0.2), (0.5, 0.15), (0.75, 0.2)]
        categories = ["Low", "Moderate", "High"]
        category_colors = colors
        
        for i, (pos, cat, col) in enumerate(zip(category_positions, categories, category_colors)):
            ax.text(pos[0], pos[1], cat, ha='center', va='center', fontsize=9,
                   color=col, fontweight='bold', zorder=3)
        
        # Draw needle
        needle_length = radius - 0.05
        dx = needle_length * np.cos(angle)
        dy = needle_length * np.sin(angle)
        
        # Needle shadow
        shadow = ax.plot([center[0], center[0] + dx], [center[1], center[1] + dy], 
                        'k-', lw=4, alpha=0.2, zorder=4)[0]
        shadow.set_path_effects([path_effects.SimpleLineShadow(), path_effects.Normal()])
        
        # Needle
        needle = ax.plot([center[0], center[0] + dx], [center[1], center[1] + dy], 
                        color='#e74c3c', lw=2.5, zorder=5)[0]
        needle.set_path_effects([path_effects.SimpleLineShadow(), path_effects.Normal()])
        
        # Center circle
        center_shadow = Circle(center, 0.03, fc='k', alpha=0.2, zorder=5)
        ax.add_patch(center_shadow)
        
        center_circle = Circle(center, 0.025, fc='#7f8c8d', ec='white', lw=1, zorder=6)
        ax.add_patch(center_circle)
        
        # Add digital display
        box_width = 0.4
        box_height = 0.15
        display_box = FancyBboxPatch((0.5 - box_width/2, 0.7), box_width, box_height, 
                                  boxstyle="round,pad=0.4", fc='white', ec=color, lw=2, 
                                  alpha=0.95, zorder=7)
        ax.add_patch(display_box)
        
        # Add risk score
        score_text = ax.text(0.5, 0.77, f"{risk_score:.1f}/10", ha='center', va='center',
                           fontsize=16, fontweight='bold', color='#2c3e50', zorder=8)
        
        # Add risk category
        cat_text = ax.text(0.5, 0.715, risk_category, ha='center', va='center',
                         fontsize=10, color=color, fontweight='bold', zorder=8)
        
        # Add title
        title_box = FancyBboxPatch((0.2, 0.85), 0.6, 0.1, boxstyle="round,pad=0.3", 
                                 fc='#34495e', ec='none', alpha=0.9, zorder=7)
        ax.add_patch(title_box)
        
        title_text = ax.text(0.5, 0.9, title, ha='center', va='center',
                           fontsize=14, fontweight='bold', color='white', zorder=8)
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    # Create individual risk gauges
    create_risk_gauge(axs[0], glucose_risk, "Glucose Risk", "glucose")
    create_risk_gauge(axs[1], bmi_risk, "Weight Risk", "default")
    create_risk_gauge(axs[2], activity_risk, "Physical Activity Risk", "activity")
    create_risk_gauge(axs[3], age_risk, "Age-Related Risk", "default")
    create_risk_gauge(axs[4], cv_risk, "Cardiovascular Risk", "cv")
    
    # Create summary section in the last panel
    axs[5].clear()
    axs[5].set_facecolor('#f8f9fa')
    
    # Add a background panel
    summary_bg = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05", 
                               fc='white', ec='#bdc3c7', lw=1, alpha=0.8, zorder=0)
    summary_bg.set_path_effects([path_effects.SimplePatchShadow(), path_effects.Normal()])
    axs[5].add_patch(summary_bg)
    
    # Add title
    title_box = FancyBboxPatch((0.1, 0.85), 0.8, 0.1, boxstyle="round,pad=0.3", 
                             fc='#34495e', ec='none', alpha=0.9, zorder=1)
    axs[5].add_patch(title_box)
    
    title_text = axs[5].text(0.5, 0.9, "Overall Health Summary", ha='center', va='center',
                           fontsize=14, fontweight='bold', color='white', zorder=2)
    
    # Determine overall risk category and color
    if overall_risk < 3.33:
        overall_color = '#2ecc71'  # Green
        overall_category = "Low Risk"
        recommendations = [
            "Maintain current healthy lifestyle",
            "Continue regular check-ups",
            "Stay physically active"
        ]
    elif overall_risk < 6.66:
        overall_color = '#f1c40f'  # Yellow
        overall_category = "Moderate Risk"
        recommendations = [
            "Increase physical activity",
            "Monitor blood glucose regularly",
            "Consider dietary adjustments"
        ]
    else:
        overall_color = '#e74c3c'  # Red
        overall_category = "High Risk"
        recommendations = [
            "Consult healthcare provider promptly",
            "Follow medication regimen strictly",
            "Make significant lifestyle changes"
        ]
    
    # Create overall risk display
    risk_box = FancyBboxPatch((0.2, 0.6), 0.6, 0.2, boxstyle="round,pad=0.4", 
                            fc='white', ec=overall_color, lw=3, alpha=0.95, zorder=1)
    axs[5].add_patch(risk_box)
    
    # Add overall risk score
    axs[5].text(0.5, 0.72, f"Overall Risk: {overall_risk:.1f}/10", ha='center', va='center',
               fontsize=16, fontweight='bold', color='#2c3e50', zorder=2)
    
    # Add risk category
    axs[5].text(0.5, 0.65, overall_category, ha='center', va='center',
               fontsize=14, color=overall_color, fontweight='bold', zorder=2)
    
    # Add recommendations section
    rec_title = axs[5].text(0.5, 0.5, "Key Recommendations:", ha='center', va='center',
                          fontsize=12, fontweight='bold', color='#2c3e50', zorder=2)
    
    # Add recommendation items
    for i, rec in enumerate(recommendations):
        y_pos = 0.42 - i * 0.08
        
        # Add bullet point
        bullet = axs[5].add_patch(Circle((0.15, y_pos), 0.015, fc=overall_color, zorder=2))
        
        # Add recommendation text
        axs[5].text(0.19, y_pos, rec, fontsize=11, va='center', ha='left', color='#2c3e50', zorder=2)
    
    # Add disclaimer
    disclaimer = axs[5].text(0.5, 0.15, "This assessment is for informational purposes only.\nConsult with healthcare professionals for medical advice.", 
                           fontsize=8, ha='center', va='center', style='italic', color='#7f8c8d', zorder=2)
    
    # Set limits and remove axes
    axs[5].set_xlim(0, 1)
    axs[5].set_ylim(0, 1)
    axs[5].axis('off')
    
    plt.tight_layout()
    fig.subplots_adjust(hspace=0.25, wspace=0.25, top=0.9)
    
    return fig

def create_health_metrics_visualizations(health_data):
    """Create simplified visualizations for key health metrics."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Extract health metrics
    fasting_glucose = health_data.get('fasting_glucose', 0)
    postmeal_glucose = health_data.get('postmeal_glucose', 0)
    hba1c = health_data.get('hba1c', 0)
    bmi = health_data.get('bmi', 0)
    
    # Create figures for each metric
    glucose_fig = create_simple_glucose_chart(fasting_glucose, postmeal_glucose)
    hba1c_fig = create_simple_hba1c_chart(hba1c)
    bmi_fig = create_simple_bmi_chart(bmi)
    
    return glucose_fig, hba1c_fig, bmi_fig

def create_simple_glucose_chart(fasting_glucose, postmeal_glucose):
    """Create a simple bar chart for glucose levels with clear boundaries."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)  # Add some padding
    
    # Define ranges and colors
    ranges = ['Normal', 'Prediabetes', 'Diabetes']
    colors = ['#2ecc71', '#f1c40f', '#e74c3c']  # Green, Yellow, Red
    
    # Define threshold values
    fasting_thresholds = [70, 100, 126, 200]
    postmeal_thresholds = [70, 140, 200, 300]
    
    # Create x positions for bars
    x = np.arange(2)
    width = 0.6
    
    # Create background bars for ranges
    for i in range(3):
        # Fasting glucose range visualization
        ax.barh(x[0], fasting_thresholds[i+1] - fasting_thresholds[i], 
               left=fasting_thresholds[i], height=width, 
               color=colors[i], alpha=0.5, edgecolor='white', linewidth=1)
        
        # Postmeal glucose range visualization
        ax.barh(x[1], postmeal_thresholds[i+1] - postmeal_thresholds[i], 
               left=postmeal_thresholds[i], height=width, 
               color=colors[i], alpha=0.5, edgecolor='white', linewidth=1)
    
    # Add values as vertical lines
    ax.axvline(x=fasting_glucose, ymin=0.25, ymax=0.45, color='black', linewidth=2)
    ax.axvline(x=postmeal_glucose, ymin=0.55, ymax=0.75, color='black', linewidth=2)
    
    # Add text for actual values
    ax.text(fasting_glucose, x[0] - 0.25, f"{fasting_glucose} mg/dL", 
           ha='center', va='center', fontweight='bold')
    ax.text(postmeal_glucose, x[1] + 0.25, f"{postmeal_glucose} mg/dL", 
           ha='center', va='center', fontweight='bold')
    
    # Set y-axis labels
    ax.set_yticks(x)
    ax.set_yticklabels(['Fasting\nGlucose', 'Post-meal\nGlucose'])
    
    # Set x-axis range and label
    ax.set_xlim(70, 300)
    ax.set_xlabel('Blood Glucose (mg/dL)')
    
    # Add title
    ax.set_title('Blood Glucose Levels', fontsize=14, fontweight='bold', pad=10)
    
    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[0], alpha=0.5, label='Normal'),
        Patch(facecolor=colors[1], alpha=0.5, label='Prediabetes'),
        Patch(facecolor=colors[2], alpha=0.5, label='Diabetes')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    # Add grid lines
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Remove y-axis spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Make top and bottom spines visible and thicker for better boundary
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['top'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)
    
    plt.tight_layout()
    
    return fig

def create_simple_hba1c_chart(hba1c):
    """Create a simple gauge chart for HbA1c with clear boundaries."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2) 
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.25)  # Add some padding
    
    # Define ranges and colors
    ranges = [(4.0, 5.6), (5.7, 6.4), (6.5, 8.0), (8.1, 10.0)]
    colors = ['#2ecc71', '#f1c40f', '#3498db', '#e74c3c']  # Green, Yellow, Blue, Red
    labels = ['Normal', 'Prediabetes', 'Target with Diabetes', 'High Risk']
    
    # Create horizontal bars for each range
    for i, (start, end) in enumerate(ranges):
        ax.barh(0, end - start, left=start, height=0.5, 
               color=colors[i], alpha=0.7, edgecolor='white', linewidth=1)
    
    # Add marker for the actual value
    ax.axvline(x=hba1c, ymin=0.25, ymax=0.75, color='black', linewidth=2)
    
    # Add text for the value
    ax.text(hba1c, 0.7, f"{hba1c}%", ha='center', va='center', 
           fontsize=14, fontweight='bold')
    
    # Set x-axis range and ticks
    ax.set_xlim(4, 10)
    ax.set_xticks([4, 5, 6, 7, 8, 9, 10])
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Add title
    #ax.set_title('HbA1c Level', fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel('HbA1c (%)')
    
    # Add a legend
    legend_elements = [
        Patch(facecolor=colors[0], alpha=0.7, label=f'{labels[0]} ({ranges[0][0]}-{ranges[0][1]}%)'),
        Patch(facecolor=colors[1], alpha=0.7, label=f'{labels[1]} ({ranges[1][0]}-{ranges[1][1]}%)'),
        Patch(facecolor=colors[2], alpha=0.7, label=f'{labels[2]} ({ranges[2][0]}-{ranges[2][1]}%)'),
        Patch(facecolor=colors[3], alpha=0.7, label=f'{labels[3]} ({ranges[3][0]}%+)')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.8, -0.25), ncol=1)
    
    # Add grid
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Make all spines visible for a clear boundary
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)
    
    plt.tight_layout()
    
    return fig

def create_simple_bmi_chart(bmi):
    """Create a simple bar chart for BMI with clear boundaries."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.25)  # Add some padding
    
    # Define BMI categories and colors
    categories = ['Underweight', 'Normal', 'Overweight', 'Obese I', 'Obese II', 'Obese III']
    ranges = [(0, 18.4), (18.5, 24.9), (25, 29.9), (30, 34.9), (35, 39.9), (40, 50)]
    colors = ['#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#9b59b6']
    
    # Create horizontal bars for each BMI category
    for i, ((start, end), color) in enumerate(zip(ranges, colors)):
        ax.barh(0, end - start, left=start, height=0.5, 
               color=color, alpha=0.7, edgecolor='white', linewidth=1)
        
        # Add category label in the middle of each section
        if end - start > 3:  # Only add text if there's enough space
            ax.text(start + (end - start)/2, 0, categories[i], 
                   ha='center', va='center', fontsize=9, color='black',
                   fontweight='bold')
    
    # Add a marker for the actual BMI value
    ax.axvline(x=bmi, ymin=0.25, ymax=0.75, color='black', linewidth=2)
    
    # Add text for the BMI value
    ax.text(bmi, 0.7, f"BMI: {bmi}", ha='center', va='center', 
           fontsize=12, fontweight='bold')
    
    # Set x-axis range and label
    ax.set_xlim(0, 50)
    ax.set_xlabel('Body Mass Index (BMI)')
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Add title
    #ax.set_title('Body Mass Index (BMI)', fontsize=14, fontweight='bold', pad=10)
    
    # Add a grid
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Make all spines visible for a clear boundary
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)
    
    # Add a legend showing the categories and their ranges
    legend_elements = []
    for i, ((start, end), color, category) in enumerate(zip(ranges, colors, categories)):
        legend_elements.append(
            Patch(facecolor=color, alpha=0.7, label=f'{category} ({start}-{end})')
        )
    
    # Place legend below the chart
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.8, -0.30), ncol=2)
    
    plt.tight_layout()
    
    return fig

def show_health_assessment():
    """Display the generated health assessment."""
    if 'health_data' not in st.session_state:
        st.warning("No health data has been entered yet. Please go to the Input Data page first.")
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="primary", use_container_width=False):
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
    #st.title("Health Assessment")
    
    # Check if assessment should be run
    run_assessment = False
    
    # Add "Run Health Assessment" button only if assessment hasn't been generated yet
    if 'health_assessment' not in st.session_state:
        run_assessment = st.button("Run Health Assessment", type="primary")
        
        if run_assessment:
            # Display loading animation while generating assessment
            with st.spinner("Analyzing your health data... This may take a moment"):
                # Generate health assessment
                assessment = generate_health_assessment(st.session_state.health_data)
                st.session_state.health_assessment = assessment
                st.rerun()  # Rerun to refresh the UI now that we have the assessment
    
    # Create tabs for different sections
    metrics_tab, assessment_tab = st.tabs(["Health Metrics", "Detailed Assessment"])
    
    with metrics_tab:
        st.header("Key Health Indicators")
        st.write("These visualizations show where your metrics stand compared to standard health ranges.")
        
        # Create visualizations
        glucose_fig, hba1c_fig, bmi_fig = create_health_metrics_visualizations(st.session_state.health_data)
        
        # Display glucose visualization
        st.markdown("---")
        st.subheader("Blood Glucose Levels")
        st.pyplot(glucose_fig)
        
        # Add a visual divider
        st.markdown("---")
        
        # Display HbA1c visualization
        st.subheader("HbA1c Levels")
        st.pyplot(hba1c_fig)
        
        # Add a visual divider
        st.markdown("---")
        
        # Display BMI visualization
        st.subheader("Body Mass Index (BMI)")
        st.pyplot(bmi_fig)
        
        # Add a visual divider
        st.markdown("---")
        
        # Add reference information
        with st.expander("Understanding Your Metrics"):
            st.markdown("""
            ### Blood Glucose
            - **Fasting Glucose**
                - Normal: 70-99 mg/dL
                - Prediabetes: 100-125 mg/dL
                - Diabetes: 126+ mg/dL
            
            - **Post-meal Glucose** (2 hours after eating)
                - Normal: <140 mg/dL
                - Prediabetes: 140-199 mg/dL
                - Diabetes: 200+ mg/dL
            
            ### HbA1c
            - Normal: 4.0-5.6%
            - Prediabetes: 5.7-6.4%
            - Diabetes: 6.5%+
            - Target for people with diabetes: typically <7.0% (individualized)
            
            ### BMI
            - Underweight: <18.5
            - Normal: 18.5-24.9
            - Overweight: 25-29.9
            - Obese Class I: 30-34.9
            - Obese Class II: 35-39.9
            - Obese Class III: 40+
            """)
    
    with assessment_tab:
        st.header("Your Health Assessment")
        
        if 'health_assessment' not in st.session_state:
            # Show message if assessment hasn't been generated yet
            st.info("Your health assessment has not been generated yet. Please go back and click the 'Run Health Assessment' button to generate your personalized assessment.")
        else:
            assessment = st.session_state.health_assessment
            
            # Process the assessment to add styling
            sections = assessment.split('\n## ')
            
            # Display first section (summary)
            st.info(sections[0])
            
            # Process and display remaining sections with dividers
            for section in sections[1:]:
                if section.strip():
                    title_end = section.find('\n')
                    title = section[:title_end].strip()
                    content = section[title_end:].strip()
                    
                    st.markdown("---")  # Add divider before each section
                    st.subheader(title)
                    
                    # Use the built-in info component
                    st.info(content)
    
    # Add disclaimer only if assessment exists
    if 'health_assessment' in st.session_state:
        st.markdown("---")
        st.info("""
        **Medical Disclaimer:** This assessment is generated by AI and is intended for informational purposes only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment. 
        Always seek the advice of your physician or other qualified health provider with any questions you may have 
        regarding your health condition.
        """)
        

def main():
    """Main function to run the Streamlit app."""
    show_header()
    
    # Get the selected page from sidebar
    page = show_sidebar()
    
    if page == "Input Data":
        show_input_data_page()
    elif page == "Nutrition Plan":
        show_nutrition_plan()
    elif page == "Educational Resources":
        show_educational_resources()
    elif page == "Health Assessment":  # New page
        show_health_assessment()

if __name__ == "__main__":
    main()