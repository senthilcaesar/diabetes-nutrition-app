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

def display_health_assessment(structured_data):
    """
    Display health assessment with consistent formatting across all sections.
    """
    # Summary section
    st.markdown("<h3 style='color:#2E7D32; margin-top:0; border-bottom:2px solid #C8E6C9; padding-bottom:10px;'>Summary</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E8F5E9; padding:15px; border-radius:5px; border-left:5px solid #4CAF50; margin-bottom:20px;">{structured_data["summary"]}</div>',
        unsafe_allow_html=True
    )
    
    # Diabetes Management Evaluation
    st.markdown("<h3 style='color:#0D47A1; margin-top:0; border-bottom:2px solid #BBDEFB; padding-bottom:10px;'>Diabetes Management Evaluation</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E3F2FD; padding:15px; border-radius:5px; border-left:5px solid #2196F3; margin-bottom:20px;">{structured_data["diabetes_management_evaluation"]}</div>',
        unsafe_allow_html=True
    )
    
    # Key Metrics Analysis
    metrics = structured_data["key_metrics_analysis"]
    
    st.markdown("<h3 style='color:#4A148C; margin-top:0; border-bottom:2px solid #E1BEE7; padding-bottom:10px;'>Key Metrics Analysis</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>Fasting Glucose:</strong> {metrics["fasting_glucose"]}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>Post-meal Glucose:</strong> {metrics["postmeal_glucose"]}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>HbA1c:</strong> {metrics["hba1c"]}</div>',
        unsafe_allow_html=True
    )
    
    # Potential Health Risks
    st.markdown("<h3 style='color:#B71C1C; margin-top:0; border-bottom:2px solid #FFCDD2; padding-bottom:10px;'>Potential Health Risks</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#FFEBEE; padding:15px; border-radius:5px; border-left:5px solid #F44336; margin-bottom:20px;">{structured_data["potential_health_risks"]}</div>',
        unsafe_allow_html=True
    )
    
    # Suggested Diagnoses and Care Plans
    st.markdown("<h3 style='color:#006064; margin-top:0; border-bottom:2px solid #B2EBF2; padding-bottom:10px;'>Suggested Diagnoses and Care Plans</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E0F7FA; padding:15px; border-radius:5px; border-left:5px solid #00BCD4; margin-bottom:20px;">{structured_data["suggested_diagnoses_and_care_plans"]}</div>',
        unsafe_allow_html=True
    )
    
    # Areas of Concern
    st.markdown("<h3 style='color:#E65100; margin-top:0; border-bottom:2px solid #FFE0B2; padding-bottom:10px;'>Areas of Concern for Discussion with a Healthcare Provider</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#FFF3E0; padding:15px; border-radius:5px; border-left:5px solid #FF9800; margin-bottom:20px;">{structured_data["areas_of_concern"]}</div>',
        unsafe_allow_html=True
    )
    
    # Recommendations as a list of points
    st.markdown("<h3 style='color:#33691E; margin-top:0; border-bottom:2px solid #DCEDC8; padding-bottom:10px;'>Recommendations for Health Management Improvement</h3>", unsafe_allow_html=True)

    # Create a styled unordered list for recommendations
    recommendations_html = '<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:20px;"><ul style="list-style-type:disc; margin-left:20px; padding-left:0;">'

    for recommendation in structured_data["recommendations"]:
        recommendations_html += f'<li style="margin-bottom:8px;">{recommendation}</li>'

    recommendations_html += '</ul></div>'

    st.markdown(recommendations_html, unsafe_allow_html=True)
    
    
def display_genetic_health_assessment(structured_data):
    """
    Display genetic health assessment with consistent formatting across all sections.
    """
    # Summary section
    st.markdown("<h3 style='color:#2E7D32; margin-top:0; border-bottom:2px solid #C8E6C9; padding-bottom:10px;'>Summary</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E8F5E9; padding:15px; border-radius:5px; border-left:5px solid #4CAF50; margin-bottom:20px;">{structured_data["summary"]}</div>',
        unsafe_allow_html=True
    )
    
    # Diabetes Management Evaluation
    st.markdown("<h3 style='color:#0D47A1; margin-top:0; border-bottom:2px solid #BBDEFB; padding-bottom:10px;'>Diabetes Management Evaluation</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E3F2FD; padding:15px; border-radius:5px; border-left:5px solid #2196F3; margin-bottom:20px;">{structured_data["diabetes_management_evaluation"]}</div>',
        unsafe_allow_html=True
    )
    
    # Key Metrics Analysis
    metrics = structured_data["key_metrics_analysis"]
    
    st.markdown("<h3 style='color:#4A148C; margin-top:0; border-bottom:2px solid #E1BEE7; padding-bottom:10px;'>Key Metrics Analysis</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>Fasting Glucose:</strong> {metrics["fasting_glucose"]}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>Post-meal Glucose:</strong> {metrics["postmeal_glucose"]}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        f'<div style="background-color:#F3E5F5; padding:15px; border-radius:5px; border-left:5px solid #9C27B0; margin-bottom:10px;"><strong>HbA1c:</strong> {metrics["hba1c"]}</div>',
        unsafe_allow_html=True
    )
    
    # Genetic Profile Overview
    st.markdown("<h3 style='color:#1A237E; margin-top:0; border-bottom:2px solid #C5CAE9; padding-bottom:10px;'>Genetic Profile Overview</h3>", unsafe_allow_html=True)
    
    # Display genetic insights if they exist in the structured data
    if "genetic_profile_overview" in structured_data:
        genetic_profile = structured_data["genetic_profile_overview"]
        
        st.markdown(
            f'<div style="background-color:#E8EAF6; padding:15px; border-radius:5px; border-left:5px solid #3F51B5; margin-bottom:10px;"><strong>Carbohydrate Metabolism:</strong> {genetic_profile["carb_metabolism"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#E8EAF6; padding:15px; border-radius:5px; border-left:5px solid #3F51B5; margin-bottom:10px;"><strong>Fat Metabolism:</strong> {genetic_profile["fat_metabolism"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#E8EAF6; padding:15px; border-radius:5px; border-left:5px solid #3F51B5; margin-bottom:10px;"><strong>Inflammation Response:</strong> {genetic_profile["inflammation_response"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#E8EAF6; padding:15px; border-radius:5px; border-left:5px solid #3F51B5; margin-bottom:20px;"><strong>Caffeine Processing:</strong> {genetic_profile["caffeine_processing"]}</div>',
            unsafe_allow_html=True
        )
    
    # Potential Health Risks
    st.markdown("<h3 style='color:#B71C1C; margin-top:0; border-bottom:2px solid #FFCDD2; padding-bottom:10px;'>Potential Health Risks</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#FFEBEE; padding:15px; border-radius:5px; border-left:5px solid #F44336; margin-bottom:20px;">{structured_data["potential_health_risks"]}</div>',
        unsafe_allow_html=True
    )
    
    # Suggested Diagnoses and Care Plans
    st.markdown("<h3 style='color:#006064; margin-top:0; border-bottom:2px solid #B2EBF2; padding-bottom:10px;'>Suggested Diagnoses and Care Plans</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#E0F7FA; padding:15px; border-radius:5px; border-left:5px solid #00BCD4; margin-bottom:20px;">{structured_data["suggested_diagnoses_and_care_plans"]}</div>',
        unsafe_allow_html=True
    )
    
    # Areas of Concern
    st.markdown("<h3 style='color:#E65100; margin-top:0; border-bottom:2px solid #FFE0B2; padding-bottom:10px;'>Areas of Concern for Discussion with a Healthcare Provider</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f'<div style="background-color:#FFF3E0; padding:15px; border-radius:5px; border-left:5px solid #FF9800; margin-bottom:20px;">{structured_data["areas_of_concern"]}</div>',
        unsafe_allow_html=True
    )
    
    # Personalized Recommendations
    st.markdown("<h3 style='color:#33691E; margin-top:0; border-bottom:2px solid #DCEDC8; padding-bottom:10px;'>Personalized Recommendations</h3>", unsafe_allow_html=True)
    
    if "personalized_recommendations" in structured_data:
        recommendations = structured_data["personalized_recommendations"]
        
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:10px;"><strong>Nutrition:</strong> {recommendations["nutrition"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:10px;"><strong>Physical Activity:</strong> {recommendations["physical_activity"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:10px;"><strong>Medication Considerations:</strong> {recommendations["medication_considerations"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:10px;"><strong>Lifestyle Modifications:</strong> {recommendations["lifestyle_modifications"]}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:20px;"><strong>Monitoring Approach:</strong> {recommendations["monitoring_approach"]}</div>',
            unsafe_allow_html=True
        )
    else:
        # If structured recommendations aren't available, use the standard recommendations field
        st.markdown(
            f'<div style="background-color:#F1F8E9; padding:15px; border-radius:5px; border-left:5px solid #8BC34A; margin-bottom:20px;">{structured_data["recommendations"]}</div>',
            unsafe_allow_html=True
        )

def show_health_assessment():
    """Display the generated health assessment."""
    if 'health_data' not in st.session_state:
        st.warning("No health data has been entered yet. Please go to the Input Data page first.")
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="primary", use_container_width=False):
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
    # Check if genetic data is available
    has_genetic_data = 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None
    
    # Check if an assessment exists
    if has_genetic_data:
        assessment_exists = 'structured_genetic_health_assessment' in st.session_state
    else:
        assessment_exists = 'structured_health_assessment' in st.session_state
    
    # Check if data has changed since last assessment
    data_changed = False
    if assessment_exists and 'last_assessed_data' in st.session_state:
        # Compare current health data with the data used for the last assessment
        current_data_hash = hash(str(st.session_state.health_data))
        last_data_hash = hash(str(st.session_state.last_assessed_data))
        
        # If genetic data is available, also check if it has changed
        if has_genetic_data and 'last_assessed_genetic_data' in st.session_state:
            current_genetic_hash = hash(str(st.session_state.genetic_profile))
            last_genetic_hash = hash(str(st.session_state.last_assessed_genetic_data))
            
            data_changed = (current_data_hash != last_data_hash) or (current_genetic_hash != last_genetic_hash)
        else:
            data_changed = (current_data_hash != last_data_hash)
    
    # Create tabs for different sections - add Genetic Insights tab if genetic data is available
    if has_genetic_data:
        metrics_tab, genetic_tab, assessment_tab = st.tabs(["Health Metrics", "Genetic Insights", "Detailed Assessment"])
    else:
        metrics_tab, assessment_tab = st.tabs(["Health Metrics", "Detailed Assessment"])
    
    # Health Metrics tab content remains the same
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
    pass

    
    with assessment_tab:
        st.header("Your Health Assessment")
        
        # Display a warning if data has changed
        if data_changed:
            st.warning("⚠️ Your health data has changed since the last assessment. Please run the health assessment again for updated results.")
        
        # Determine appropriate button text based on context
        if data_changed:
            button_text = "Re-run Assessment"
        elif not assessment_exists:
            button_text = "Run Health Assessment" if not has_genetic_data else "Run Genetic Health Assessment"
        else:
            button_text = "Run Health Assessment Again" if not has_genetic_data else "Run Genetic Health Assessment Again"
        
        # Single button for all assessment generation cases
        run_assessment = st.button(button_text, type="primary")
        
        if run_assessment:
            # Display loading animation while generating assessment
            with st.spinner("Analyzing your health data... This may take a moment"):
                # Generate health assessment based on availability of genetic data
                if has_genetic_data:
                    generate_genetic_health_assessment(
                        st.session_state.health_data, 
                        st.session_state.genetic_profile, 
                        st.secrets["OPENAI_API_KEY"]
                    )
                    # Store copies of the data
                    st.session_state.last_assessed_data = st.session_state.health_data.copy()
                    st.session_state.last_assessed_genetic_data = st.session_state.genetic_profile.copy()
                else:
                    generate_health_assessment(
                        st.session_state.health_data, 
                        st.secrets["OPENAI_API_KEY"]
                    )
                    # Store a copy of the data
                    st.session_state.last_assessed_data = st.session_state.health_data.copy()
                
                # Force a rerun to refresh the UI
                st.rerun()
        
        # Display the appropriate assessment based on what's available
        if has_genetic_data and 'structured_genetic_health_assessment' in st.session_state:
            display_genetic_health_assessment(st.session_state.structured_genetic_health_assessment)
        elif 'structured_health_assessment' in st.session_state:
            display_health_assessment(st.session_state.structured_health_assessment)
        else:
            # Show message if assessment hasn't been generated yet
            if has_genetic_data:
                st.info("Click the 'Run Genetic Health Assessment' button to generate your personalized assessment incorporating genetic insights.")
            else:
                st.info("Click the 'Run Health Assessment' button to generate your personalized assessment.")
    
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
            pass

            