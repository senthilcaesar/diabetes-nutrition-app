import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import os
from PIL import Image
import io
import base64
import time
import openai
from openai import OpenAI

# Add at the top of app.py
from utils.data_processing import preprocess_health_data, preprocess_socioeconomic_data
from utils.llm_integration import DiabetesNutritionAI
from utils.visualization import (create_pictogram_food_guide, create_simple_meal_pairing_guide, create_symptom_response_guide)

# Set page configuration
st.set_page_config(
    page_title="Personalized Diabetes Nutrition Plan",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OpenAI API configuration
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store this securely in Streamlit secrets

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
    return nutrition_plan

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


# UI Components
def show_header():
    """Display the application header."""
    st.title("Personalized Diabetes Nutrition Plan")
    st.markdown("""
    This application creates personalized nutrition plans for individuals with diabetes, 
    taking into account health metrics, socioeconomic factors, and cultural preferences.
    """)
    st.markdown("---")

def show_sidebar():
    """Configure and display the sidebar."""
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to", ["Input Data", "View Plan", "Educational Resources"])
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application was developed to provide accessible, 
        personalized nutrition guidance for individuals with diabetes, 
        particularly those in underserved communities.
        """)
        
        st.markdown("---")
        st.markdown("Developed by: [Your Organization]")
    
    return page

def input_health_data():
    """Collect health-related data from the user."""
    st.header("Health Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=120, value=45)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=170.0, step=0.1)
        
        # Calculate BMI
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        st.metric("BMI", bmi, help="Body Mass Index")
        
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"],
            value="Moderately Active"
        )
    
    with col2:
        diabetes_type = st.selectbox("Diabetes Type", ["Type 1", "Type 2", "Gestational", "Prediabetes"])
        fasting_glucose = st.number_input("Fasting Blood Glucose (mg/dL)", min_value=70, max_value=300, value=120)
        postmeal_glucose = st.number_input("Post-meal Blood Glucose (mg/dL)", min_value=70, max_value=400, value=160)
        hba1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=14.0, value=7.0, step=0.1)
        
        st.subheader("Additional Health Information")
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Gluten-Free", "Lactose Intolerant", "Nut Allergies", "Shellfish Allergies"]
        )
        medications = st.text_area("Current Medications (one per line)")
        other_conditions = st.text_area("Other Health Conditions (one per line)")
    
    # Collect the data into a dictionary
    health_data = {
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
    
    return health_data

def input_socioeconomic_data():
    """Collect socioeconomic data from the user."""
    st.header("Socioeconomic and Cultural Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Location (Country/Region)")
        geographic_setting = st.selectbox("Geographic Setting", ["Urban", "Suburban", "Rural"])
        income_level = st.select_slider(
            "Income Level",
            options=["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"],
            value="Middle"
        )
        education_level = st.selectbox(
            "Education Level",
            ["Elementary/Primary", "High School/Secondary", "College/University", "Graduate/Professional"]
        )
        literacy_level = st.select_slider(
            "Literacy Level",
            options=["Low", "Basic", "Moderate", "High"],
            value="Moderate"
        )
    
    with col2:
        language_preferences = st.text_input("Preferred Language(s)")
        technology_access = st.select_slider(
            "Access to Technology",
            options=["Very Limited", "Limited", "Moderate", "Good", "Excellent"],
            value="Moderate"
        )
        healthcare_access = st.select_slider(
            "Access to Healthcare",
            options=["Very Limited", "Limited", "Moderate", "Good", "Excellent"],
            value="Moderate"
        )
        local_food_availability = st.selectbox(
            "Local Food Availability",
            ["Limited", "Moderate", "Abundant"]
        )
        grocery_budget = st.select_slider(
            "Grocery Budget",
            options=["Very Limited", "Limited", "Moderate", "Comfortable", "Generous"],
            value="Moderate"
        )
    
    st.subheader("Living Situation and Food Preferences")
    
    col3, col4 = st.columns(2)
    
    with col3:
        cooking_facilities = st.multiselect(
            "Cooking Facilities Available",
            ["Basic stove", "Oven", "Microwave", "Refrigerator", "Freezer", "Limited/Shared kitchen", "No cooking facilities"]
        )
        meal_prep_time = st.select_slider(
            "Time Available for Meal Preparation",
            options=["Very Limited", "Limited", "Moderate", "Substantial"],
            value="Limited"
        )
    
    with col4:
        family_size = st.number_input("Family Size (including yourself)", min_value=1, max_value=20, value=1)
        support_system = st.multiselect(
            "Support System",
            ["Lives alone", "Family support", "Community support", "Healthcare support", "Limited support"]
        )
        cultural_foods = st.text_area("Cultural Food Preferences and Traditional Foods")
    
    # Collect the data into a dictionary
    socio_data = {
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
    
    return socio_data

def show_input_data_page():
    """Display the input data collection page."""
    health_data_tab, socio_data_tab, submit_tab = st.tabs(["Health Information", "Socioeconomic Information", "Generate Plan"])
    
    with health_data_tab:
        if 'health_data' not in st.session_state:
            st.session_state.health_data = {}
        
        st.session_state.health_data = input_health_data()
        
        if st.button("Save Health Information", key="save_health"):
            st.success("Health information saved! Please proceed to the Socioeconomic Information tab.")
    
    with socio_data_tab:
        if 'socio_data' not in st.session_state:
            st.session_state.socio_data = {}
        
        st.session_state.socio_data = input_socioeconomic_data()
        
        if st.button("Save Socioeconomic Information", key="save_socio"):
            st.success("Socioeconomic information saved! Please proceed to Generate Plan tab.")
    
    with submit_tab:
        st.header("Generate Your Personalized Nutrition Plan")
        
        if 'health_data' in st.session_state and 'socio_data' in st.session_state:
            st.info("Review your information before generating the plan:")
            
            show_button = st.button("Show Collected Data")
            if show_button:
                st.subheader("Health Information")
                st.json(st.session_state.health_data)
                
                st.subheader("Socioeconomic Information")
                st.json(st.session_state.socio_data)
            
            if st.button("Generate Personalized Nutrition Plan", key="generate_plan"):
                with st.spinner("Generating your personalized nutrition plan... This may take up to a minute."):
                    # Preprocess the data
                    processed_health_data = preprocess_health_data(st.session_state.health_data)
                    processed_socio_data = preprocess_socioeconomic_data(st.session_state.socio_data)
                    
                    # Combine the data
                    combined_data = {**processed_health_data, **processed_socio_data}
                    
                    # Generate the nutrition plan
                    try:
                        nutrition_plan = generate_nutrition_plan(combined_data)
                        st.session_state.nutrition_plan = nutrition_plan
                        
                        # Generate visual guidance
                        visual_guidance = generate_visual_guidance(
                            nutrition_plan, 
                            combined_data.get('literacy_level', 'moderate'),
                            combined_data.get('plan_complexity', 'moderate')
                        )
                        st.session_state.visual_guidance = visual_guidance
                        
                        st.success("Your personalized nutrition plan has been generated! Go to the View Plan page to see it.")
                    except Exception as e:
                        st.error(f"An error occurred while generating the plan: {str(e)}")
        else:
            st.warning("Please complete both the Health Information and Socioeconomic Information tabs before generating a plan.")

def show_nutrition_plan():
    """Display the generated nutrition plan."""
    if 'nutrition_plan' not in st.session_state:
        st.warning("No nutrition plan has been generated yet. Please go to the Input Data page first.")
        return
    
    st.header("Your Personalized Diabetes Nutrition Plan")
    
    # Display the plan in tabs for better organization
    overview_tab, meal_plan_tab, recipes_tab, visuals_tab = st.tabs(["Overview", "Meal Plan", "Recipes & Tips", "Visual Guides"])
    
    # Split the nutrition plan into sections
    nutrition_plan = st.session_state.nutrition_plan
    sections = nutrition_plan.split("\n## ")
    sections = ["## " + section if i > 0 else section for i, section in enumerate(sections)]
    
    # Extract main sections
    overview_sections = [s for s in sections if any(x in s.lower() for x in ["introduction", "overview", "caloric", "macronutrient", "recommendation"])]
    meal_plan_sections = [s for s in sections if any(x in s.lower() for x in ["meal plan", "sample meal", "day 1", "day 2", "day 3"])]
    recipe_sections = [s for s in sections if any(x in s.lower() for x in ["recipe", "tips", "avoid", "limit", "portion", "guideline"])]
    
    with overview_tab:
        for section in overview_sections:
            st.markdown(section)
    
    with meal_plan_tab:
        for section in meal_plan_sections:
            st.markdown(section)
    
    with recipes_tab:
        for section in recipe_sections:
            st.markdown(section)
    
    with visuals_tab:
        if 'visual_guidance' in st.session_state:
            st.subheader("Visual Guides")
            st.markdown(st.session_state.visual_guidance)
            
            # Here you would normally generate actual visuals based on the descriptions
            # For demonstration, we'll just show a placeholder
            st.info("In a production environment, these visual descriptions would be converted to actual images.")
            
            # Example visual - Portion Size Guide
            def create_sample_portion_guide():
                fig, axs = plt.subplots(1, 3, figsize=(12, 4))
                
                # Protein portion
                axs[0].text(0.5, 0.5, "Protein\nPalm-sized", ha='center', va='center', fontsize=14)
                axs[0].set_title("Protein Portion", fontsize=16)
                axs[0].axis('off')
                
                # Carbs portion
                axs[1].text(0.5, 0.5, "Carbs\nFist-sized", ha='center', va='center', fontsize=14)
                axs[1].set_title("Carbohydrate Portion", fontsize=16)
                axs[1].axis('off')
                
                # Vegetables portion
                axs[2].text(0.5, 0.5, "Vegetables\nTwo hands", ha='center', va='center', fontsize=14)
                axs[2].set_title("Vegetable Portion", fontsize=16)
                axs[2].axis('off')
                
                plt.tight_layout()
                return fig
            
            st.pyplot(create_sample_portion_guide())
            
            # Example visual - Blood Glucose Target Range
            def create_sample_glucose_guide():
                fig, ax = plt.subplots(figsize=(10, 3))
                
                # Create a range
                ax.axhspan(0, 1, xmin=0, xmax=0.3, color='#F44336', alpha=0.3)  # Red for low
                ax.axhspan(0, 1, xmin=0.3, xmax=0.7, color='#4CAF50', alpha=0.3)  # Green for target
                ax.axhspan(0, 1, xmin=0.7, xmax=1, color='#F44336', alpha=0.3)  # Red for high
                
                # Add labels
                ax.text(0.15, 0.5, "LOW\n< 70 mg/dL", ha='center', va='center', fontsize=12)
                ax.text(0.5, 0.5, "TARGET RANGE\n70-180 mg/dL", ha='center', va='center', fontsize=14, fontweight='bold')
                ax.text(0.85, 0.5, "HIGH\n> 180 mg/dL", ha='center', va='center', fontsize=12)
                
                ax.set_title("Blood Glucose Target Range", fontsize=16)
                ax.axis('off')
                
                return fig
            
            st.pyplot(create_sample_glucose_guide())
        else:
            st.warning("No visual guidance has been generated yet.")
    
    # Add download button for the plan
    st.download_button(
        label="Download Nutrition Plan (PDF)",
        data="This would be a generated PDF in a production environment",  # In production this would be the PDF
        file_name="diabetes_nutrition_plan.pdf",
        mime="application/pdf"
    )

def show_educational_resources():
    """Display educational resources about diabetes nutrition."""
    st.header("Educational Resources")
    
    resource_type = st.radio(
        "Select Resource Type",
        ["Diabetes Basics", "Food & Nutrition", "Physical Activity", "Monitoring", "Cultural Adaptations"]
    )
    
    if resource_type == "Diabetes Basics":
        st.subheader("Understanding Diabetes")
        
        st.markdown("""
        ### What is Diabetes?
        Diabetes is a chronic condition that affects how your body turns food into energy. There are several types:
        
        - **Type 1 Diabetes**: The body doesn't produce insulin. This is usually diagnosed in children and young adults.
        - **Type 2 Diabetes**: The body doesn't use insulin properly. This is the most common type.
        - **Gestational Diabetes**: Develops during pregnancy in women who don't already have diabetes.
        - **Prediabetes**: Blood sugar is higher than normal but not high enough to be diagnosed as type 2 diabetes.
        
        ### How Diabetes Affects Your Body
        When you eat, your body turns food into glucose (sugar) that enters your bloodstream. Your pancreas releases insulin to help move glucose from the blood into cells for energy. With diabetes, either your body doesn't make enough insulin or can't use it effectively, leading to high blood sugar levels.
        
        ### Importance of Blood Sugar Management
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
            ### Blood Sugar Targets
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
    
    elif resource_type == "Food & Nutrition":
        st.subheader("Nutrition for Diabetes Management")
        
        st.markdown("""
        ### Key Principles of Diabetes Nutrition
        
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
            ### Glycemic Index and Load
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
    
    elif resource_type == "Physical Activity":
        st.subheader("Physical Activity and Diabetes")
        
        st.markdown("""
        ### Benefits of Physical Activity for Diabetes
        
        Regular physical activity:
        - Lowers blood glucose by increasing insulin sensitivity
        - Helps maintain a healthy weight
        - Reduces cardiovascular disease risk
        - Improves mood and reduces stress
        - Strengthens muscles and bones
        
        ### Recommended Activity
        
        - **Aim for 150 minutes of moderate-intensity activity per week**
        - Spread activity throughout the week (e.g., 30 minutes, 5 days a week)
        - Include both aerobic exercise and strength training
        - Start slowly and gradually increase intensity
        
        ### Types of Physical Activity
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
        ### Safety Tips
        
        - Check blood glucose before, during (for long sessions), and after activity
        - Carry fast-acting carbs (like glucose tablets) in case of low blood sugar
        - Stay hydrated
        - Wear proper footwear and inspect feet after activity
        - Start with low intensity and gradually increase
        - Talk to your healthcare provider before starting a new exercise program
        """)
    
    elif resource_type == "Monitoring":
        st.subheader("Monitoring Blood Glucose")
        
        st.markdown("""
        ### Why Monitor Blood Glucose?
        
        Regular monitoring helps you:
        - Understand how food, activity, medication, and stress affect your blood sugar
        - Detect patterns and make adjustments to your management plan
        - Prevent or address high and low blood sugar episodes
        - Track your progress toward goals
        - Make informed decisions about food, activity, and medication
        
        ### When to Check Blood Glucose
        
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
            ### Understanding Your Results
            
            General target ranges (may vary based on provider recommendations):
            
            - **Before meals**: 80-130 mg/dL
            - **1-2 hours after meals**: Less than 180 mg/dL
            - **Bedtime**: 100-140 mg/dL
            
            **HbA1c**: Measures average blood sugar over 2-3 months
            - Target for most adults with diabetes: Less than 7%
            
            ### Responding to Results
            
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
    
    elif resource_type == "Cultural Adaptations":
        st.subheader("Cultural Adaptations for Diabetes Management")
        
        region = st.selectbox(
            "Select a Region for Cultural Adaptations",
            ["African Cuisine", "South Asian Cuisine", "Latin American Cuisine", "Middle Eastern Cuisine", "East Asian Cuisine"]
        )
        
        if region == "African Cuisine":
            st.markdown("""
            ### Adapting African Diets for Diabetes Management
            
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
            ### Adapting South Asian Diets for Diabetes Management
            
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
            ### Adapting Latin American Diets for Diabetes Management
            
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
            ### Adapting Middle Eastern Diets for Diabetes Management
            
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
            ### Adapting East Asian Diets for Diabetes Management
            
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
        ### General Principles for Cultural Adaptation
        
        1. **Preserve Cultural Identity**: Modify traditional dishes rather than eliminate them
        2. **Use Traditional Wisdom**: Many cultures have traditional foods that are beneficial for diabetes
        3. **Focus on Cooking Methods**: Often changing preparation method is easier than changing the food itself
        4. **Portion Control**: Sometimes enjoying smaller amounts of traditional foods is the best approach
        5. **Community Involvement**: Include family and community in dietary changes for better support
        """)

def main():
    """Main function to run the Streamlit app."""
    show_header()
    page = show_sidebar()
    
    if page == "Input Data":
        show_input_data_page()
    elif page == "View Plan":
        show_nutrition_plan()
    elif page == "Educational Resources":
        show_educational_resources()

if __name__ == "__main__":
    main()
