"""
Main application file for the Personalized Diabetes Nutrition Plan.
This file serves as the entry point and handles navigation between pages.
"""

import streamlit as st

# Now use absolute imports
from utils.ui_components import show_header, apply_custom_css, show_sidebar
from app_pages.input_page import show_input_data_page
from app_pages.nutrition_plan_page import show_nutrition_plan
from app_pages.health_assessment_page import show_health_assessment
from app_pages.educational_resources_page import show_educational_resources
from app_pages.rag_qa_page import show_rag_qa_page

# Set page configuration
st.set_page_config(
    page_title="Diabetes Nutrition Plan",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function to run the Streamlit app."""
    # Display header
    # show_header()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Get the selected page from sidebar
    page = show_sidebar()
    
    # Display the selected page
    if page == "Input Data":
        show_input_data_page()
    elif page == "Nutrition Plan":
        show_nutrition_plan()
    elif page == "Health Assessment":
        show_health_assessment()
    elif page == "Educational Resources":
        show_educational_resources()
    elif page == "Q&A":
        show_rag_qa_page()

if __name__ == "__main__":
    main()
