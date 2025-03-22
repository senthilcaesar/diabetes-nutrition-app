"""
Health assessment page for the Diabetes Nutrition Plan application.
Displays health metrics and the AI-generated health assessment.
"""

import streamlit as st
from utils.visualization import create_health_metrics_visualizations
from utils.llm_integration import generate_health_assessment

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
    
    # Check if assessment should be run
    run_assessment = False
    
    # Add "Run Health Assessment" button only if assessment hasn't been generated yet
    if 'health_assessment' not in st.session_state:
        run_assessment = st.button("Run Health Assessment", type="primary")
    else:
        run_assessment = st.button("Run Health Assessment Again", type="primary")
        
    if run_assessment:
        # Display loading animation while generating assessment
        with st.spinner("Analyzing your health data... This may take a moment"):
            # Generate health assessment
            assessment = generate_health_assessment(st.session_state.health_data, st.secrets["OPENAI_API_KEY"])
            st.session_state.health_assessment = assessment
            
            # Store a copy of the data used for this assessment
            st.session_state.last_assessed_data = st.session_state.health_data.copy()
            st.rerun()  # Rerun to refresh the UI now that we have the assessment
    
    # Rest of your function remains the same...
    
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
                    
                    #st.markdown("---")  # Add divider before each section
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