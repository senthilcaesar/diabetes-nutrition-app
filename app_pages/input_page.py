"""
Input data page for the Diabetes Nutrition Plan application.
Handles user input for health and socioeconomic data.
"""

import streamlit as st
import time

# Import from utils directory
from utils.data_processing import combine_user_data
from utils.ui_components import input_health_data, input_socioeconomic_data, navigate_to_view_plan
from utils.llm_integration import generate_nutrition_plan, generate_visual_guidance

def display_user_data_review():
    """Display a review of the user's health and socioeconomic data."""
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
            
            # Format and display medications
            medications = health_data.get('medications', '')
            if medications:
                formatted_medications = medications.replace('\n', ', ').replace(',,', ',').strip(',')
                display_text = formatted_medications[:50] + "..." if len(formatted_medications) > 50 else formatted_medications
                st.write("**Current Medications:**", display_text)
            else:
                st.write("**Current Medications:** None")

            # Format and display other conditions
            other_conditions = health_data.get('other_conditions', '')
            if other_conditions:
                formatted_conditions = other_conditions.replace('\n', ', ').replace(',,', ',').strip(',')
                display_text = formatted_conditions[:50] + "..." if len(formatted_conditions) > 50 else formatted_conditions
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
            cultural_foods = socio_data.get('cultural_foods', '')
            st.write("**Cultural Foods:**", cultural_foods[:50] + "..." if len(cultural_foods) > 50 else cultural_foods)

def generate_nutrition_plan_workflow():
    """Handle the workflow for generating the nutrition plan."""
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
        
        # Combine the data
        try:
            # Combine user data
            combined_data = combine_user_data(st.session_state.health_data, st.session_state.socio_data)
            progress_bar.progress(95/100)
            percentage_text.markdown("<div style='text-align: center;'><strong>95% Complete</strong></div>", unsafe_allow_html=True)
            
            # Generate the nutrition plan
            nutrition_plan = generate_nutrition_plan(combined_data, st.secrets["OPENAI_API_KEY"])
            st.session_state.nutrition_plan = nutrition_plan
            progress_bar.progress(98/100)
            percentage_text.markdown("<div style='text-align: center;'><strong>98% Complete</strong></div>", unsafe_allow_html=True)
            
            # Generate visual guidance
            visual_guidance = generate_visual_guidance(
                nutrition_plan, 
                combined_data.get('literacy_level', 'moderate'),
                combined_data.get('plan_complexity', 'moderate'),
                st.secrets["OPENAI_API_KEY"]
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

def show_input_data_page():
    """Show the input data page with tabs for health and socioeconomic information."""
    # Create tabs
    tab_titles = ["🩺 Health Information", "🏘️ Socioeconomic Information", "🚀 Generate Plan"]
    tabs = st.tabs(tab_titles)
    
    with tabs[0]:
        st.markdown("")
        
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
                display_user_data_review()
            
            if generate_button:
                generate_nutrition_plan_workflow()
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