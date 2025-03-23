"""
Health assessment page for the Diabetes Nutrition Plan application.
Displays health metrics, genetic insights, and the AI-generated health assessment.
"""

import streamlit as st
from utils.visualization import create_health_metrics_visualizations
from utils.llm_integration import generate_health_assessment
from utils.genetic_ui_components import show_genetic_insights
from utils.genetic_llm_integration import generate_genetic_health_assessment

"""
Health assessment page for the Diabetes Nutrition Plan application.
Displays health metrics, genetic insights, and the AI-generated health assessment.
"""

import streamlit as st
from utils.visualization import create_health_metrics_visualizations
from utils.llm_integration import generate_health_assessment
from utils.genetic_ui_components import show_genetic_insights
from utils.genetic_llm_integration import generate_genetic_health_assessment

def show_health_assessment():
    """Display the generated health assessment."""
    if 'health_data' not in st.session_state:
        st.warning("No health data has been entered yet. Please go to the Input Data page first.")
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="primary", use_container_width=False):
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
    # Check if data has changed since last assessment
    if 'health_assessment' in st.session_state and 'last_assessed_data' in st.session_state:
        # Compare current health data with the data used for the last assessment
        current_data_hash = hash(str(st.session_state.health_data))
        last_data_hash = hash(str(st.session_state.last_assessed_data))
        
        if current_data_hash != last_data_hash:
            st.warning("⚠️ Your health data has changed since the last assessment. Please run the health assessment again for updated results.")
    
    # Check if genetic data is available
    has_genetic_data = 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None
    
    # Create tabs for different sections - add Genetic Insights tab if genetic data is available
    if has_genetic_data:
        metrics_tab, genetic_tab, assessment_tab = st.tabs(["Health Metrics", "Genetic Insights", "Detailed Assessment"])
    else:
        metrics_tab, assessment_tab = st.tabs(["Health Metrics", "Detailed Assessment"])
    
    with metrics_tab:
        st.header("Key Health Indicators")
        st.write("These visualizations show where your metrics stand compared to standard health ranges.")
        
        # Create visualizations
        glucose_fig, hba1c_fig, bmi_fig = create_health_metrics_visualizations(st.session_state.health_data)
        
        # Display glucose visualization
        #st.markdown("---")
        st.subheader("Blood Glucose Levels")
        st.pyplot(glucose_fig)
        
        # Add a visual divider
        #st.markdown("---")
        
        # Display HbA1c visualization
        st.subheader("HbA1c Levels")
        st.pyplot(hba1c_fig)
        
        # Add a visual divider
        #st.markdown("---")
        
        # Display BMI visualization
        st.subheader("Body Mass Index (BMI)")
        st.pyplot(bmi_fig)
        
        # Add a visual divider
        #st.markdown("---")
        
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
            
            # Add "Run Health Assessment" button inside the Detailed Assessment tab
            if 'health_assessment' not in st.session_state:
                button_text = "Run Health Assessment" if not has_genetic_data else "Run Genetic Health Assessment"
                run_assessment = st.button(button_text, type="primary", key="run_health_assessment_button")
            else:
                button_text = "Run Health Assessment Again" if not has_genetic_data else "Run Genetic Health Assessment Again"
                run_assessment = st.button(button_text, type="primary", key="run_health_assessment_again_button")
            
            if run_assessment:
                # Display loading animation while generating assessment
                with st.spinner("Analyzing your health data... This may take a moment"):
                    # Generate health assessment based on availability of genetic data
                    if has_genetic_data:
                        assessment = generate_genetic_health_assessment(
                            st.session_state.health_data, 
                            st.session_state.genetic_profile, 
                            st.secrets["OPENAI_API_KEY"]
                        )
                    else:
                        assessment = generate_health_assessment(
                            st.session_state.health_data, 
                            st.secrets["OPENAI_API_KEY"]
                        )
                        
                    st.session_state.health_assessment = assessment
                    
                    # Store a copy of the data used for this assessment
                    st.session_state.last_assessed_data = st.session_state.health_data.copy()
                    st.rerun()  # Rerun to refresh the UI now that we have the assessment
            
            if 'health_assessment' not in st.session_state:
                # Show message if assessment hasn't been generated yet
                if has_genetic_data:
                    st.info("Click the 'Run Genetic Health Assessment' button to generate your personalized assessment incorporating genetic insights.")
                else:
                    st.info("Click the 'Run Health Assessment' button to generate your personalized assessment.")
            else:
                assessment = st.session_state.health_assessment
                
                # Process the assessment to add styling
                if '\n## ' in assessment:
                    sections = assessment.split('\n## ')
                    # Display first section (summary)
                    st.info(sections[0])
                    
                    # Process and display remaining sections with dividers
                    for section in sections[1:]:
                        if section.strip():
                            title_end = section.find('\n')
                            if title_end > 0:  # Make sure there's a newline
                                title = section[:title_end].strip()
                                content = section[title_end:].strip()
                                
                                st.markdown(f"### {title}")
                                st.info(content)
                else:
                    # If the assessment doesn't have clear sections, just display it all
                    st.info(assessment)
    
  # Show genetic insights tab if genetic data is available
    if has_genetic_data:
        with genetic_tab:
            st.header("Your Genetic Insights")
            
            if 'genetic_profile' not in st.session_state:
                st.info("No genetic profile available. Please upload genetic data on the Input Data page.")
                return
            
            # Check if genetic insights should be displayed
            if 'show_genetic_insights' not in st.session_state:
                st.session_state.show_genetic_insights = False
            
            # Add button to view genetic insights
            view_insights = st.button(
                "View Genetic Insights", 
                type="primary",
                key="view_genetic_insights_button",
                help="Click to view detailed insights based on your genetic profile"
            )
            
            if view_insights:
                st.session_state.show_genetic_insights = True
                st.rerun()
            
            # Only show detailed genetic insights if the button has been clicked
            if st.session_state.show_genetic_insights:
                genetic_profile = st.session_state.genetic_profile
                
                # Display overall summary
                st.markdown("### Genetic Profile Summary")
                st.info(genetic_profile.get('overall_summary', 'No genetic summary available.'))
                
                # Create columns for the main genetic factors
                col1, col2 = st.columns(2)
                
                # Column 1: Carbohydrate and Fat Metabolism
                with col1:
                    # Carbohydrate Metabolism Section
                    st.markdown("### Carbohydrate Metabolism")
                    carb_data = genetic_profile.get("carb_metabolism", {})
                    
                    # Display carb sensitivity with colored indicator
                    sensitivity = carb_data.get('carb_sensitivity', 'normal').title()
                    sensitivity_color = "#4CAF50" if sensitivity == "Normal" else "#FFC107" if sensitivity == "Higher" else "#F44336"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #F1F8E9; 
                        border-left: 5px solid {sensitivity_color};
                        padding: 15px; 
                        border-radius: 4px;
                        margin: 10px 0;
                    ">
                        <h4 style="margin-top: 0; color: #2E7D32;">Carbohydrate Sensitivity: {sensitivity}</h4>
                        <p>{carb_data.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    st.markdown("#### Recommendations")
                    for rec in carb_data.get("recommendations", []):
                        st.markdown(f"- {rec}")
                    
                    # Fat Metabolism Section
                    st.markdown("### Fat Metabolism")
                    fat_data = genetic_profile.get("fat_metabolism", {})
                    
                    # Display fat sensitivity with colored indicator
                    fat_sensitivity = fat_data.get('saturated_fat_sensitivity', 'normal').title()
                    fat_color = "#4CAF50" if fat_sensitivity == "Normal" else "#FFC107" if fat_sensitivity == "Moderate" else "#F44336"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #FFF8E1; 
                        border-left: 5px solid {fat_color};
                        padding: 15px; 
                        border-radius: 4px;
                        margin: 10px 0;
                    ">
                        <h4 style="margin-top: 0; color: #FF8F00;">Saturated Fat Sensitivity: {fat_sensitivity}</h4>
                        <p>{fat_data.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    st.markdown("#### Recommendations")
                    for rec in fat_data.get("recommendations", []):
                        st.markdown(f"- {rec}")
                
                # Column 2: Other Genetic Factors
                with col2:
                    # Vitamin Metabolism Section
                    st.markdown("### Nutrient Processing")
                    nutrient_data = genetic_profile.get("vitamin_metabolism", {})
                    
                    # Display folate processing with colored indicator
                    folate_processing = nutrient_data.get('folate_processing', 'normal').title()
                    folate_color = "#4CAF50" if folate_processing == "Normal" else "#FFC107" if folate_processing == "Reduced" else "#F44336"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #E8F5E9; 
                        border-left: 5px solid {folate_color};
                        padding: 15px; 
                        border-radius: 4px;
                        margin: 10px 0;
                    ">
                        <h4 style="margin-top: 0; color: #388E3C;">Folate Processing: {folate_processing}</h4>
                        <p>{nutrient_data.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    st.markdown("#### Recommendations")
                    for rec in nutrient_data.get("recommendations", []):
                        st.markdown(f"- {rec}")
                    
                    # Inflammation Response Section
                    st.markdown("### Inflammation Response")
                    inflammation_data = genetic_profile.get("inflammation_response", {})
                    
                    # Display inflammation response with colored indicator
                    inflammation_response = inflammation_data.get('inflammatory_response', 'normal').title()
                    inflammation_color = "#4CAF50" if inflammation_response == "Normal" else "#FFC107" if inflammation_response == "Moderate" else "#F44336"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #FFEBEE; 
                        border-left: 5px solid {inflammation_color};
                        padding: 15px; 
                        border-radius: 4px;
                        margin: 10px 0;
                    ">
                        <h4 style="margin-top: 0; color: #D32F2F;">Inflammatory Response: {inflammation_response}</h4>
                        <p>{inflammation_data.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    st.markdown("#### Recommendations")
                    for rec in inflammation_data.get("recommendations", []):
                        st.markdown(f"- {rec}")
                    
                    # Caffeine Metabolism Section
                    st.markdown("### Caffeine Metabolism")
                    caffeine_data = genetic_profile.get("caffeine_metabolism", {})
                    
                    # Display caffeine metabolism with colored indicator
                    caffeine_metabolism = caffeine_data.get('caffeine_metabolism', 'normal').title()
                    caffeine_color = "#4CAF50" if caffeine_metabolism == "Fast" else "#FFC107" if caffeine_metabolism == "Normal" else "#F44336"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #E0F7FA; 
                        border-left: 5px solid {caffeine_color};
                        padding: 15px; 
                        border-radius: 4px;
                        margin: 10px 0;
                    ">
                        <h4 style="margin-top: 0; color: #0097A7;">Caffeine Metabolism: {caffeine_metabolism}</h4>
                        <p>{caffeine_data.get('explanation', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendations
                    st.markdown("#### Recommendations")
                    for rec in caffeine_data.get("recommendations", []):
                        st.markdown(f"- {rec}")
                
                # Add a note about the genetic assessment
                st.markdown("---")
                st.markdown("""
                ### About Genetic-Based Nutrition
                
                Your genetic profile has been analyzed for markers related to metabolism and nutrition.
                The results shown above indicate how your genetic variants may influence your body's
                response to different types of foods and nutrients.
                
                These insights are incorporated into your health assessment and nutrition plan to provide
                more personalized recommendations based on your unique genetic profile.
                
                *Note: Genetic factors are just one aspect of health. Your nutrition plan also considers
                your current health status, lifestyle factors, and personal preferences.*
                """)
                
                # Add disclaimer
                st.info("""
                **Genetic Analysis Disclaimer**: This assessment is based on current understanding of genetics and nutrition science.
                Individual responses may vary. This information is not intended to diagnose, treat, cure, or prevent any disease.
                Always consult with healthcare providers for medical advice.
                """)
            else:
                # Show a brief preview with an invitation to view detailed insights
                st.info("""
                Your genetic profile is available. Click the "View Genetic Insights" button above to see detailed information about:
                
                - Carbohydrate Metabolism
                - Fat Metabolism
                - Nutrient Processing
                - Inflammation Response
                - Caffeine Metabolism
                
                These insights will help you understand how your genetic variants may influence your nutritional needs.
                """)