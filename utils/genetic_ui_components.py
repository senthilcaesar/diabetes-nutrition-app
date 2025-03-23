"""
Genetic UI components module for the Diabetes Nutrition Plan application.
Contains UI components for genetic data input and visualization.
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import base64
import io
import tempfile
import os
from typing import Dict, List, Optional, Tuple, Any

from utils.genetic_processing import (
    load_genetic_data, 
    generate_genetic_nutrition_profile,
    create_sample_genetic_data
)
from utils.genetic_processing import DIABETES_GENETIC_MARKERS

def input_genetic_data() -> Dict:
    """
    Collect genetic data from the user.
    
    Returns:
        Dict: Dictionary containing user genetic data or empty if not provided
    """
    # Create a container for the genetic data section
    genetic_container = st.container()
    
    with genetic_container:
        st.subheader("Genetic Data (Optional)")
        
        # Initialize genetic_profile in session state if not present
        if 'genetic_profile' not in st.session_state:
            st.session_state.genetic_profile = None
            
        # Initialize genetic_data_option in session state if not present
        if 'genetic_data_option' not in st.session_state:
            st.session_state.genetic_data_option = "None"
        
       # Ask the user how they want to provide genetic data
        genetic_data_option = st.radio(
            "Would you like to incorporate genetic data for more personalized recommendations?",
            options=["None", "Upload genetic data file", "Use sample data for demonstration"],
            index=["None", "Upload genetic data file", "Use sample data for demonstration"].index(
                st.session_state.genetic_data_option),
            key="genetic_data_option_radio"  # Added unique key here
        )
        st.session_state.genetic_data_option = genetic_data_option
        
        genetic_data = {}
        
        if genetic_data_option == "Upload genetic data file":
            # File uploader for genetic data
            uploaded_file = st.file_uploader(
                "Upload your genetic data (23andMe, Ancestry, or VCF format)",
                type=["txt", "csv", "vcf", "json"],
                key="genetic_file_uploader"
            )
            
            if uploaded_file is not None:
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_filepath = tmp_file.name
                
                # Store the uploaded file content for display
                uploaded_content = uploaded_file.getvalue().decode('utf-8', errors='replace')
                
                # Process the genetic data
                with st.spinner("Processing genetic data..."):
                    try:
                        genetic_data = load_genetic_data(tmp_filepath)
                        if genetic_data:
                            st.success(f"Successfully processed genetic data with {len(genetic_data)} markers.")
                            
                            # Store the original genetic data in session state for use in other tabs
                            st.session_state.original_genetic_data = genetic_data
                            
                            # Display the raw data in an expandable section
                            with st.expander("View Raw Genetic Data", expanded=False):
                                # Create a DataFrame for better display
                                import pandas as pd
                                
                                # Initialize data list
                                data_list = []
                                
                                # Convert genetic_data dict to DataFrame
                                for marker, genotype in genetic_data.items():
                                    # Find gene name for this marker
                                    gene_name = "Unknown"
                                    for gene, markers in DIABETES_GENETIC_MARKERS.items():
                                        if marker in markers:
                                            gene_name = gene
                                            break
                                    
                                    data_list.append({
                                        "Marker ID": marker,
                                        "Genotype": genotype,
                                        "Gene": gene_name,
                                    })
                                
                                # Create and display DataFrame
                                df = pd.DataFrame(data_list)
                                st.dataframe(df, use_container_width=True)
                                
                                # Add a download button for the processed data
                                st.download_button(
                                    label="Download Processed Genetic Data",
                                    data=df.to_csv(index=False),
                                    file_name="processed_genetic_data.csv",
                                    mime="text/csv",
                                    key="download_genetic_data"
                                )
                            
                            # Display the original uploaded file content
                            with st.expander("View Uploaded File Content", expanded=False):
                                # Display first 100 lines or 5000 characters, whichever is less
                                lines = uploaded_content.split('\n')
                                if len(lines) > 100:
                                    displayed_content = '\n'.join(lines[:100]) + "\n\n... (file continues)"
                                elif len(uploaded_content) > 5000:
                                    displayed_content = uploaded_content[:5000] + "\n\n... (file continues)"
                                else:
                                    displayed_content = uploaded_content
                                
                                st.text(displayed_content)
                            
                            # Generate genetic profile
                            genetic_profile = generate_genetic_nutrition_profile(genetic_data)
                            st.session_state.genetic_profile = genetic_profile
                            
                            # Display a preview of the genetic profile
                            with st.expander("Preview Genetic Profile", expanded=True):
                                st.markdown(f"**Overall Summary:** {genetic_profile['overall_summary']}")
                                
                                st.markdown("**Key Recommendations:**")
                                for i, rec in enumerate(genetic_profile['key_recommendations']):
                                    st.markdown(f"- {rec}")
                        else:
                            st.error("No genetic markers were found in the uploaded file. Please check the file format.")
                    except Exception as e:
                        st.error(f"Error processing genetic data: {str(e)}")
                    finally:
                        # Clean up the temporary file
                        try:
                            os.unlink(tmp_filepath)
                        except:
                            pass
        
        elif genetic_data_option == "Use sample data for demonstration":
            # Use sample data for demonstration
            with st.spinner("Generating sample genetic profile..."):
                # Define the sample file path
                sample_file_path = "example_data/sample_23andme.txt"
                
                try:
                    # Load from the sample file
                    genetic_data = load_genetic_data(sample_file_path)
                    
                    if genetic_data:
                        st.success(f"Successfully loaded sample genetic data with {len(genetic_data)} markers.")
                        
                        # Store the original genetic data in session state for use in other tabs
                        st.session_state.original_genetic_data = genetic_data

                        
                        # Display the sample data in an expandable section
                        with st.expander("View Sample Genetic Data", expanded=True):
                            # Create a DataFrame for better display
                            import pandas as pd
                            
                            # Initialize data list
                            data_list = []
                            
                            for marker, genotype in genetic_data.items():
                                # Find gene name for this marker
                                gene_name = "Unknown"
                                for gene, markers in DIABETES_GENETIC_MARKERS.items():
                                    if marker in markers:
                                        gene_name = gene
                                        break
                                
                                # Add entry to our data list
                                data_list.append({
                                    "Marker ID": marker,
                                    "Genotype": genotype,
                                    "Gene": gene_name,
                                })
                            
                            # Create and display DataFrame
                            df = pd.DataFrame(data_list)
                            st.dataframe(df, use_container_width=True)
                        
                        # Display the file content in a separate expander
                        # Display the file content in a separate expander
                        with st.expander("Raw Sample File Content", expanded=False):
                            # Use the same sample_file_path that was used to load the data
                            try:
                                with open(sample_file_path, "r") as file:
                                    sample_content = file.read()
                                st.text(sample_content)
                            except FileNotFoundError:
                                st.error(f"Sample file not found: {sample_file_path}")
                                st.info("Make sure you have created the example_data directory and placed the sample_23andme.txt file there.")
                            except Exception as e:
                                st.error(f"Error reading sample file: {str(e)}")
                                st.info("You may need to check if the file exists and has proper permissions.")
                        
                        # Generate genetic profile
                        genetic_profile = generate_genetic_nutrition_profile(genetic_data)
                        st.session_state.genetic_profile = genetic_profile
                        
                        # Display a preview of the genetic profile
                        with st.expander("Preview Sample Genetic Profile", expanded=True):
                            st.info("This is a sample genetic profile using data from the file: example_data/sample_23andme.txt")
                            st.markdown(f"**Overall Summary:** {genetic_profile['overall_summary']}")
                            
                            st.markdown("**Key Recommendations:**")
                            for i, rec in enumerate(genetic_profile['key_recommendations']):
                                st.markdown(f"- {rec}")
                    else:
                        st.error("No genetic markers were found in the sample file. Please check the file format.")
                        # Fallback to programmatically generated sample data
                        genetic_data = create_sample_genetic_data()
                        genetic_profile = generate_genetic_nutrition_profile(genetic_data)
                        st.session_state.genetic_profile = genetic_profile
                except Exception as e:
                    st.error(f"Error loading sample genetic data: {str(e)}")
                    # Fallback to the programmatic sample data if file loading fails
                    st.warning("Falling back to programmatically generated sample data.")
                    genetic_data = create_sample_genetic_data()
                    genetic_profile = generate_genetic_nutrition_profile(genetic_data)
                    st.session_state.genetic_profile = genetic_profile
        
        elif genetic_data_option == "None":
            # Clear genetic profile if user selects "None"
            st.session_state.genetic_profile = None
            st.info("No genetic data will be used for generating recommendations.")
        
        # Add information about benefits and privacy
        with st.expander("About Genetic-Based Nutrition", expanded=False):
            st.markdown("""
            ### Benefits of Genetic-Based Nutrition
            
            Incorporating genetic data allows us to provide more personalized nutrition recommendations based on your unique genetic profile. This can help:
            
            - Optimize your carbohydrate intake based on your metabolism
            - Understand your sensitivity to different types of fats
            - Identify potential micronutrient needs
            - Tailor recommendations for inflammation management
            - Provide insights on caffeine metabolism and its effects on blood glucose
            
            ### Privacy and Data Security
            
            Your genetic data privacy is extremely important to us:
            
            - All genetic data is processed locally and is not stored on our servers
            - We only analyze specific markers related to nutrition and metabolism
            - Your genetic information will never be shared with third parties
            - You can delete your genetic data at any time
            """)
    
    return genetic_data

def show_genetic_insights():
    """
    Display genetic insights and visualizations.
    """
    if 'genetic_profile' not in st.session_state or st.session_state.genetic_profile is None:
        st.info("No genetic data has been provided. To see personalized genetic insights, please upload your genetic data or use sample data on the Input Data page.")
        return
    
    genetic_profile = st.session_state.genetic_profile
    
    # Create a container for the genetic insights
    st.subheader("Personalized Genetic Insights")
    
    # Display the overall summary
    st.markdown(f"**Overall Assessment:** {genetic_profile['overall_summary']}")
    
    # Create tabs for different categories
    tab_names = ["Carbohydrate Metabolism", "Fat Metabolism", "Nutrient Processing", "Inflammation", "Caffeine Response"]
    tabs = st.tabs(tab_names)
    
    # Tab 1: Carbohydrate Metabolism
    with tabs[0]:
        carb_data = genetic_profile["carb_metabolism"]
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Carbohydrate Sensitivity")
            st.markdown(f"**Status:** {carb_data['carb_sensitivity'].title()}")
            st.markdown(f"**What this means:** {carb_data['explanation']}")
            
            st.markdown("### Recommendations")
            for rec in carb_data["recommendations"]:
                st.markdown(f"- {rec}")
        
        with col2:
            # Create a visualization for carbohydrate sensitivity
            fig = create_carb_sensitivity_visualization(carb_data["carb_sensitivity"])
            st.pyplot(fig)
            
            # Add information about carb sources
            st.markdown("### Favorable Carbohydrate Sources")
            if carb_data["carb_sensitivity"] == "high":
                st.markdown("""
                - Non-starchy vegetables
                - Berries (in moderation)
                - Legumes
                - Small amounts of whole grains
                """)
            elif carb_data["carb_sensitivity"] == "higher":
                st.markdown("""
                - Whole grains (moderate portions)
                - Legumes
                - Most fruits (moderate portions)
                - Non-starchy vegetables
                """)
            else:
                st.markdown("""
                - Whole grains
                - Fruits
                - Legumes
                - Non-starchy vegetables
                """)
    
    # Tab 2: Fat Metabolism
    with tabs[1]:
        fat_data = genetic_profile["fat_metabolism"]
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Saturated Fat Sensitivity")
            st.markdown(f"**Status:** {fat_data['saturated_fat_sensitivity'].title()}")
            st.markdown(f"**What this means:** {fat_data['explanation']}")
            
            st.markdown("### Recommendations")
            for rec in fat_data["recommendations"]:
                st.markdown(f"- {rec}")
        
        with col2:
            # Create a visualization for fat sensitivity
            fig = create_fat_sensitivity_visualization(fat_data["saturated_fat_sensitivity"])
            st.pyplot(fig)
            
            # Add information about fat sources
            st.markdown("### Recommended Fat Sources")
            if fat_data["saturated_fat_sensitivity"] == "high":
                st.markdown("""
                - Olive oil
                - Avocados
                - Nuts and seeds
                - Fatty fish
                """)
            elif fat_data["saturated_fat_sensitivity"] == "moderate":
                st.markdown("""
                - Olive oil
                - Avocados
                - Nuts and seeds
                - Limited dairy
                - Lean proteins
                """)
            else:
                st.markdown("""
                - Balanced mix of fats
                - Moderate amounts of dairy
                - Olive oil
                - Avocados
                - Nuts and seeds
                """)
    
    # Tab 3: Nutrient Processing
    with tabs[2]:
        nutrient_data = genetic_profile["vitamin_metabolism"]
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Folate Processing Ability")
            st.markdown(f"**Status:** {nutrient_data['folate_processing'].title()}")
            st.markdown(f"**What this means:** {nutrient_data['explanation']}")
            
            st.markdown("### Recommendations")
            for rec in nutrient_data["recommendations"]:
                st.markdown(f"- {rec}")
        
        with col2:
            # Add information about nutrient sources
            st.markdown("### Top Folate Sources")
            if nutrient_data["folate_processing"] == "significantly reduced":
                st.markdown("""
                - Leafy greens (spinach, kale, collards)
                - Liver
                - Asparagus
                - Brussels sprouts
                - Avocados
                """)
            elif nutrient_data["folate_processing"] == "reduced":
                st.markdown("""
                - Leafy greens
                - Legumes (lentils, chickpeas)
                - Broccoli
                - Citrus fruits
                - Fortified foods
                """)
            else:
                st.markdown("""
                - Various fruits and vegetables
                - Whole grains
                - Legumes
                - Fortified foods
                """)
    
    # Tab 4: Inflammation
    with tabs[3]:
        inflammation_data = genetic_profile["inflammation_response"]
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Inflammatory Response")
            st.markdown(f"**Status:** {inflammation_data['inflammatory_response'].title()}")
            st.markdown(f"**What this means:** {inflammation_data['explanation']}")
            
            st.markdown("### Recommendations")
            for rec in inflammation_data["recommendations"]:
                st.markdown(f"- {rec}")
        
        with col2:
            # Add information about anti-inflammatory foods
            st.markdown("### Top Anti-Inflammatory Foods")
            if inflammation_data["inflammatory_response"] == "elevated":
                st.markdown("""
                - Fatty fish (salmon, sardines)
                - Berries
                - Turmeric with black pepper
                - Green tea
                - Extra virgin olive oil
                - Cruciferous vegetables
                """)
            elif inflammation_data["inflammatory_response"] == "moderate":
                st.markdown("""
                - Fatty fish
                - Colorful fruits and vegetables
                - Olive oil
                - Nuts and seeds
                - Green tea
                """)
            else:
                st.markdown("""
                - Balanced diet with variety of whole foods
                - Colorful fruits and vegetables
                - Healthy fats
                - Lean proteins
                """)
    
    # Tab 5: Caffeine Response
    with tabs[4]:
        caffeine_data = genetic_profile["caffeine_metabolism"]
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Caffeine Metabolism")
            st.markdown(f"**Status:** {caffeine_data['caffeine_metabolism'].title()}")
            st.markdown(f"**What this means:** {caffeine_data['explanation']}")
            
            st.markdown("### Recommendations")
            for rec in caffeine_data["recommendations"]:
                st.markdown(f"- {rec}")
        
        with col2:
            # Create a visualization for caffeine metabolism
            fig = create_caffeine_metabolism_visualization(caffeine_data["caffeine_metabolism"])
            st.pyplot(fig)
            
            # Add information about caffeine sources
            st.markdown("### Caffeine Considerations")
            if caffeine_data["caffeine_metabolism"] == "slow" or caffeine_data["caffeine_metabolism"] == "very slow":
                st.markdown("""
                **Sources to be mindful of:**
                - Coffee
                - Tea
                - Energy drinks
                - Some medications
                - Chocolate
                
                **Timing recommendation:**
                Avoid caffeine after 12pm
                """)
            else:
                st.markdown("""
                **Common caffeine sources:**
                - Coffee
                - Tea
                - Energy drinks
                - Some medications
                - Chocolate
                
                **Timing recommendation:**
                Avoid caffeine after 2-4pm
                """)
    
    # Add a note about integrating with the nutrition plan
    st.markdown("---")
    st.info("These genetic insights have been integrated into your personalized nutrition plan recommendations.")

def create_carb_sensitivity_visualization(sensitivity_level):
    """
    Create a visualization for carbohydrate sensitivity.
    
    Args:
        sensitivity_level (str): Carbohydrate sensitivity level
        
    Returns:
        matplotlib.figure.Figure: A figure showing carbohydrate sensitivity
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Setup meter properties
    meter_width = 0.2
    y_pos = 0.5
    
    # Create meter background
    ax.add_patch(patches.Rectangle((0.1, y_pos-meter_width/2), 0.8, meter_width, 
                                  facecolor='#e0e0e0', edgecolor='none', alpha=0.5))
    
    # Define sensitivity levels and colors
    sensitivity_levels = {"normal": 0.2, "higher": 0.5, "high": 0.8}
    colors = {"normal": "#4CAF50", "higher": "#FFC107", "high": "#F44336"}
    
    # Create color gradient
    for i, (level, position) in enumerate(sensitivity_levels.items()):
        if i > 0:
            prev_level = list(sensitivity_levels.keys())[i-1]
            prev_pos = sensitivity_levels[prev_level]
            gradient_width = position - prev_pos
            ax.add_patch(patches.Rectangle((0.1 + prev_pos, y_pos-meter_width/2), 
                                          gradient_width, meter_width, 
                                          facecolor=colors[level], edgecolor='none', alpha=0.7))
    
    # Add labels
    for level, position in sensitivity_levels.items():
        ax.text(0.1 + position, y_pos - meter_width/2 - 0.07, level.upper(), 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add current position marker
    marker_pos = 0.1 + sensitivity_levels.get(sensitivity_level, 0.2)
    ax.add_patch(patches.Circle((marker_pos, y_pos), 0.03, facecolor='black'))
    ax.add_patch(patches.Circle((marker_pos, y_pos), 0.025, facecolor=colors.get(sensitivity_level, "#4CAF50")))
    
    # Add title
    ax.text(0.5, 0.9, "CARBOHYDRATE SENSITIVITY", ha='center', va='center', 
           fontsize=14, fontweight='bold')
    
    # Add description
    if sensitivity_level == "high":
        description = "You may be more sensitive to carbohydrates,\nrequiring careful attention to quality and portion size."
    elif sensitivity_level == "higher":
        description = "You have moderately increased sensitivity to carbohydrates,\nfocus on quality and moderate portions."
    else:
        description = "Your carbohydrate metabolism appears typical,\nfocus on balanced intake of quality carbohydrates."
    
    ax.text(0.5, 0.2, description, ha='center', va='center', fontsize=9)
    
    # Set limits and remove axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    return fig

def create_fat_sensitivity_visualization(sensitivity_level):
    """
    Create a visualization for fat sensitivity.
    
    Args:
        sensitivity_level (str): Fat sensitivity level
        
    Returns:
        matplotlib.figure.Figure: A figure showing fat sensitivity
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Define fat types and proportions
    fat_types = ["Saturated", "Monounsaturated", "Polyunsaturated"]
    
    # Determine proportions based on sensitivity level
    if sensitivity_level == "high":
        proportions = [15, 45, 40]  # Lower saturated fat
    elif sensitivity_level == "moderate":
        proportions = [20, 45, 35]  # Moderate saturated fat
    else:
        proportions = [25, 40, 35]  # Typical saturated fat
    
    # Colors for each fat type
    colors = ["#F44336", "#4CAF50", "#2196F3"]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(proportions, labels=fat_types, colors=colors,
                                     autopct='%1.0f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    
    # Enhance text appearance
    for text in texts:
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_color('white')
    
    # Add title
    ax.text(0, 1.3, "RECOMMENDED FAT DISTRIBUTION", ha='center', va='center', 
           fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    # Add sensitivity level
    ax.text(0, 1.15, f"Based on {sensitivity_level.upper()} saturated fat sensitivity", 
           ha='center', va='center', fontsize=10, transform=ax.transAxes)
    
    # Equal aspect ratio ensures pie chart is circular
    ax.set_aspect('equal')
    
    return fig

def create_caffeine_metabolism_visualization(metabolism_rate):
    """
    Create a visualization for caffeine metabolism.
    
    Args:
        metabolism_rate (str): Caffeine metabolism rate
        
    Returns:
        matplotlib.figure.Figure: A figure showing caffeine metabolism
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Define metabolism rates and corresponding half-lives
    metabolism_rates = {"fast": 4, "normal": 5, "slow": 8, "very slow": 12}
    
    # Get half-life for the given metabolism rate
    half_life = metabolism_rates.get(metabolism_rate, 5)
    
    # Create time points for the curve
    time_points = np.linspace(0, 12, 100)
    
    # Calculate caffeine levels over time (exponential decay)
    caffeine_levels = 100 * np.exp(-np.log(2) * time_points / half_life)
    
    # Plot the caffeine metabolism curve
    ax.plot(time_points, caffeine_levels, linewidth=3, color="#795548")
    
    # Fill under the curve
    ax.fill_between(time_points, 0, caffeine_levels, color="#795548", alpha=0.3)
    
    # Add a horizontal line at 50% to show half-life
    ax.axhline(y=50, linestyle='--', color='#9E9E9E', alpha=0.7)
    ax.text(0.2, 52, "50% Caffeine Remaining", fontsize=8, color='#616161')
    
    # Mark the half-life point
    ax.plot([half_life, half_life], [0, 50], linestyle='--', color='#9E9E9E', alpha=0.7)
    ax.text(half_life, 5, f"{half_life} hours", fontsize=8, ha='center', color='#616161')
    
    # Add labels and title
    ax.set_xlabel("Hours After Consumption")
    ax.set_ylabel("Caffeine Remaining (%)")
    ax.set_title(f"Caffeine Metabolism Rate: {metabolism_rate.title()}", fontweight='bold')
    
    # Set axis limits
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 105)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Add annotations
    if metabolism_rate == "fast":
        ax.text(6, 80, "Your body processes caffeine quickly", ha='center', fontsize=9)
    elif metabolism_rate == "slow":
        ax.text(6, 80, "Your body processes caffeine slowly", ha='center', fontsize=9)
    elif metabolism_rate == "very slow":
        ax.text(6, 80, "Your body processes caffeine very slowly", ha='center', fontsize=9)
    
    plt.tight_layout()
    
    return fig