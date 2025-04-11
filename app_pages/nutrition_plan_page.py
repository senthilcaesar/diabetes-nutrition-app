"""
Nutrition plan page for the Diabetes Nutrition Plan application.
Displays the generated nutrition plan, genetic optimization, and visual guidance.
"""

import streamlit as st
import re
from datetime import datetime
from utils.visualization import (
    create_enhanced_portion_guide,
    create_enhanced_glucose_guide,
    create_foods_to_avoid_visual,
    create_recommended_foods_visual
)

def show_nutrition_plan():
    """Display the generated nutrition plan."""
    if 'nutrition_plan' not in st.session_state:
        st.warning("No nutrition plan has been generated yet. Please go to the Input Data page first.")
        
        st.markdown("""
        <style>
        /* Style for the active tab (primary button) */
        .stButton button[kind="primary"] {
            background-color: #87CEEB !important; /* Sky blue */
            color: #333333 !important; /* Dark gray for text */
            border-color: #000000 !important; /* Black border */
            font-weight: 600 !important;
        }
        
        /* Hover effect for inactive tabs */
        .stButton button[kind="secondary"]:hover {
            background-color: #E5E4E2 !important; /* Very light blue on hover */
            color: #333333 !important; /* Dark gray for text */
            border-color: #000000 !important; /* Black border */
            font-weight: 600 !important;
        }
        
        </style>
""", unsafe_allow_html=True)
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="secondary", use_container_width=False):
            # Set a navigation flag instead of directly changing radio value
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
    # Get the nutrition plan from session state
    nutrition_plan = st.session_state.nutrition_plan
    
    # Check if genetic data is available
    has_genetic_data = 'genetic_profile' in st.session_state and st.session_state.genetic_profile is not None
    
    # Display the plan in tabs for better organization - add a genetic tab if genetic data is used
    if has_genetic_data:
        overview_tab, meal_plan_tab, genetic_tab, recipes_tab, visuals_tab = st.tabs([
            "Overview", "Meal Plan", "Genetic Optimization", "Recipes & Tips", "Visual Guides"
        ])
    else:
        overview_tab, meal_plan_tab, recipes_tab, visuals_tab = st.tabs([
            "Overview", "Meal Plan", "Recipes & Tips", "Visual Guides"
        ])
    
    # Display genetic badge at the top if genetic data is used
    # Overview tab content
    with overview_tab:
                
        # Add download button at the top of the overview tab
        html_content = create_nutrition_plan_html()
        if html_content:
            st.download_button(
                label="📥 Download Nutrition Plan",
                data=html_content,
                file_name="diabetes_nutrition_plan.html",
                mime="text/html",
                key="download_nutrition_plan",
                help="Download your nutrition plan as an HTML file that you can open in any browser and print to PDF"
            )             
        
        # Display genetic badge at the top if genetic data is used
            
        if 'nutrition_overview' in st.session_state:
            st.markdown(st.session_state.nutrition_overview, unsafe_allow_html=True)
        else:
            # Fall back to extracting from the complete plan if separate sections aren't available
            overview_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "introduction", "overview", "caloric", "macronutrient", "recommended"
            ])]
            for section in overview_sections:
                st.markdown(section, unsafe_allow_html=True)
    
    # Meal Plan tab content
    with meal_plan_tab:
        # For genetic plans, add a small indicator that this is genetically optimized
            
        if 'nutrition_meal_plan' in st.session_state:
            st.markdown(st.session_state.nutrition_meal_plan, unsafe_allow_html=True)
        else:
            # Fall back to extracting from the complete plan
            meal_plan_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "meal plan", "sample meal", "day 1", "day 2", "day 3"
            ])]
            for section in meal_plan_sections:
                st.markdown(section, unsafe_allow_html=True)
    
    # Genetic Optimization tab (only shown if genetic data is available)
    if has_genetic_data:
        with genetic_tab:
            
            # If we have the dedicated genetic section from the structured plan, use it
            if 'nutrition_genetic_section' in st.session_state:
                st.markdown(st.session_state.nutrition_genetic_section, unsafe_allow_html=True)
            else:
                # If no structured genetic section is available, try to find relevant sections
                # from the complete plan or fall back to the genetic profile
                genetic_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                    "genetic", "gene", "dna", "nutrigenomics", "personalized metabolism"
                ])]
                
                if genetic_sections:
                    for section in genetic_sections:
                        st.markdown(section, unsafe_allow_html=True)
                else:
                    # If no explicit genetic sections found, display genetic profile information
                    genetic_profile = st.session_state.genetic_profile
                    
                    st.subheader("Your Genetic Profile Summary")
                    st.info(genetic_profile.get('overall_summary', 'No genetic summary available.'))
                    
                    st.subheader("How Your Nutrition Plan Has Been Optimized")
                    
                    # Create columns for each major genetic factor
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Carbohydrate Metabolism")
                        carb_data = genetic_profile.get("carb_metabolism", {})
                        st.markdown(f"**Your Profile:** {carb_data.get('carb_sensitivity', 'Normal').title()}")
                        st.markdown(f"**What this means:** {carb_data.get('explanation', '')}")
                        
                        st.markdown("#### Fat Metabolism")
                        fat_data = genetic_profile.get("fat_metabolism", {})
                        st.markdown(f"**Your Profile:** {fat_data.get('saturated_fat_sensitivity', 'Normal').title()} sensitivity to saturated fats")
                        st.markdown(f"**What this means:** {fat_data.get('explanation', '')}")
                    
                    with col2:
                        st.markdown("#### Inflammation Response")
                        inflammation_data = genetic_profile.get("inflammation_response", {})
                        st.markdown(f"**Your Profile:** {inflammation_data.get('inflammatory_response', 'Normal').title()}")
                        st.markdown(f"**What this means:** {inflammation_data.get('explanation', '')}")
                        
                        st.markdown("#### Caffeine Metabolism")
                        caffeine_data = genetic_profile.get("caffeine_metabolism", {})
                        st.markdown(f"**Your Profile:** {caffeine_data.get('caffeine_metabolism', 'Normal').title()}")
                        st.markdown(f"**What this means:** {caffeine_data.get('explanation', '')}")
                
                    st.subheader("Food Recommendations Based on Your Genetic Profile")
                    st.markdown("""
                    | Category | Recommended Foods based on Genetics |
                    |----------|-------------------------------------|
                    | **Carbohydrates** | Whole grains, legumes, vegetables (personalized based on your carbohydrate metabolism) |
                    | **Proteins** | Lean proteins, fatty fish (optimized for your inflammatory profile) |
                    | **Fats** | Olive oil, avocados, nuts (tailored to your fat metabolism) |
                    | **Supplements to Consider** | B-vitamins, omega-3 fatty acids (based on your genetic profile) |
                    """)
                    
                    st.subheader("Key Recommendations Based on Your Genetic Profile")
                    for i, rec in enumerate(genetic_profile.get('key_recommendations', [])):
                        st.markdown(f"- {rec}")
                    
                    # Add genetic nutrition disclaimer
                    st.markdown("""
                    ### Genetic Nutrition Disclaimer
                    
                    The genetic optimization suggestions provided are based on a limited set of genetic markers and current scientific understanding, which continues to evolve. Individual responses may vary, and these recommendations should be considered as complementary to standard diabetes management practices.
                    
                    Always consult with healthcare providers before making significant changes to your diet or lifestyle based on genetic information.
                    """)
    
    # Recipes & Tips tab content
    with recipes_tab:
        if 'nutrition_recipes_tips' in st.session_state:
            st.markdown(st.session_state.nutrition_recipes_tips, unsafe_allow_html=True)
        else:
            # Fall back to extracting from the complete plan
            recipe_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "recipe", "tips", "avoid", "limit", "portion", "guideline", "stabilize"
            ]) and not any(x in s.lower() for x in ["genetic", "gene", "dna"])]
            for section in recipe_sections:
                st.markdown(section, unsafe_allow_html=True)
            
    # Visual Guides tab content
    with visuals_tab:
        if 'visual_guidance' in st.session_state:
            display_visual_guidance(has_genetic_data)
        else:
            st.warning("No visual guidance has been generated yet.")

def create_nutrition_plan_html():
    """
    Create an HTML version of the nutrition plan that can be easily printed to PDF.
    """
    try:
        # Import markdown library for conversion
        import markdown
        
        # Get the nutrition plan from session state
        nutrition_plan = st.session_state.nutrition_plan
        
        # Get current date
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Create HTML content with proper styling for printing
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Diabetes Nutrition Plan</title>
            <style>
                @page {{ size: letter; margin: 1cm; }}
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3, h4 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                }}
                h1 {{
                    text-align: center;
                    color: #3498db;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .date {{
                    color: #7f8c8d;
                    font-style: italic;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 30px;
                    page-break-inside: avoid;
                }}
                .footer {{
                    margin-top: 50px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #7f8c8d;
                    border-top: 1px solid #eee;
                    padding-top: 20px;
                }}
                ul, ol {{
                    margin-left: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                hr {{
                    border: 0;
                    height: 1px;
                    background: #ddd;
                    margin: 20px 0;
                }}
                .emoji {{
                    font-size: 1.2em;
                }}
                @media print {{
                    body {{
                        font-size: 12pt;
                    }}
                    h1 {{
                        font-size: 18pt;
                    }}
                    h2 {{
                        font-size: 16pt;
                    }}
                    h3 {{
                        font-size: 14pt;
                    }}
                    .no-print {{
                        display: none;
                    }}
                    @page {{
                        margin: 2cm;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Personalized Diabetes Nutrition Plan</h1>
                <p class="date">Generated on {current_date}</p>
            </div>
        """
        
        # Function to convert markdown to HTML
        def convert_markdown_to_html(markdown_text):
            # Clean up HTML tags that might be in the text
            cleaned_text = re.sub(r'<.*?>', '', markdown_text)
            
            # Process bold text manually (** ** format)
            def process_bold(text):
                # Replace **text** with <strong>text</strong>
                bold_pattern = r'\*\*(.*?)\*\*'
                return re.sub(bold_pattern, r'<strong>\1</strong>', text)
            
            # Process headers manually (# format)
            def process_headers(text):
                # Replace # Header with <h1>Header</h1>, ## Header with <h2>Header</h2>, etc.
                lines = []
                for line in text.split('\n'):
                    if line.strip().startswith('#'):
                        # Count the number of # characters
                        header_level = 0
                        for char in line:
                            if char == '#':
                                header_level += 1
                            else:
                                break
                        
                        if header_level > 0 and header_level <= 6:
                            # Extract the header text
                            header_text = line[header_level:].strip()
                            # Create the HTML header
                            line = f'<h{header_level}>{header_text}</h{header_level}>'
                    lines.append(line)
                return '\n'.join(lines)
            
            # Process lists manually (- or * format)
            def process_lists(text):
                lines = []
                in_list = False
                
                for line in text.split('\n'):
                    stripped = line.strip()
                    if stripped.startswith('- ') or stripped.startswith('* '):
                        if not in_list:
                            lines.append('<ul>')
                            in_list = True
                        # Extract the list item text
                        item_text = stripped[2:].strip()
                        lines.append(f'<li>{item_text}</li>')
                    else:
                        if in_list:
                            lines.append('</ul>')
                            in_list = False
                        lines.append(line)
                
                if in_list:
                    lines.append('</ul>')
                
                return '\n'.join(lines)
            
            # Convert markdown tables to HTML tables
            def process_tables(text):
                table_pattern = r'\|(.+)\|\n\|[-:| ]+\|\n((?:\|.+\|\n)+)'
                
                def table_replacement(match):
                    header = match.group(1).strip()
                    rows = match.group(2).strip()
                    
                    # Process header
                    header_cells = [cell.strip() for cell in header.split('|')]
                    header_html = '<tr>' + ''.join([f'<th>{cell}</th>' for cell in header_cells if cell]) + '</tr>'
                    
                    # Process rows
                    rows_html = ''
                    for row in rows.split('\n'):
                        if '|' in row:
                            cells = [cell.strip() for cell in row.split('|')]
                            rows_html += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in cells if cell]) + '</tr>'
                    
                    return f'<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">{header_html}{rows_html}</table>'
                
                return re.sub(table_pattern, table_replacement, text, flags=re.MULTILINE)
            
            # Process horizontal rules (---)
            def process_hr(text):
                hr_pattern = r'^---+$'
                return re.sub(hr_pattern, '<hr>', text, flags=re.MULTILINE)
            
            # Process paragraphs and line breaks
            def process_paragraphs(text):
                # Split text into paragraphs (double line breaks)
                paragraphs = text.split('\n\n')
                processed_paragraphs = []
                
                for paragraph in paragraphs:
                    # Skip empty paragraphs
                    if not paragraph.strip():
                        continue
                    
                    # Check if this is a special element (header, list, table, etc.)
                    if paragraph.strip().startswith('#') or paragraph.strip().startswith('|') or \
                       paragraph.strip().startswith('- ') or paragraph.strip().startswith('* ') or \
                       paragraph.strip() == '---':
                        # Don't wrap these in <p> tags
                        processed_paragraphs.append(paragraph)
                    else:
                        # Handle line breaks within paragraphs
                        lines = paragraph.split('\n')
                        processed_lines = []
                        
                        for line in lines:
                            if line.strip():
                                processed_lines.append(line)
                        
                        # Join lines with <br> tags and wrap in <p> tags
                        if processed_lines:
                            processed_paragraph = '<p>' + '<br>'.join(processed_lines) + '</p>'
                            processed_paragraphs.append(processed_paragraph)
                
                return '\n'.join(processed_paragraphs)
            
            # Apply all the processing functions
            processed_text = cleaned_text
            processed_text = process_bold(processed_text)
            processed_text = process_headers(processed_text)
            processed_text = process_lists(processed_text)
            processed_text = process_tables(processed_text)
            processed_text = process_hr(processed_text)
            processed_text = process_paragraphs(processed_text)
            
            # Replace emoji codes with actual emojis
            emoji_map = {
                '🔥': '🔥', '🥗': '🥗', '⏱️': '⏱️', '🌾': '🌾',
                '🥩': '🥩', '🥑': '🥑', '🥦': '🥦', '🍎': '🍎',
                '🥤': '🥤', '🌞': '🌞', '🥪': '🥪', '🍲': '🍲',
                '🍏': '🍏', '🍽️': '🍽️', '🥛': '🥛', '📉': '📉', 
                '📈': '📈', '⏰': '⏰', '🥕': '🥕', '🍞': '🍞',
                '🍟': '🍟', '🥓': '🥓', '🍰': '🍰', '☕': '☕',
                '🍗': '🍗', '🫒': '🫒', '🫘': '🫘', '🐟': '🐟',
                '🫐': '🫐', '🥬': '🥬'
            }
            
            # Replace emoji text with actual emojis
            for emoji_text, emoji in emoji_map.items():
                processed_text = processed_text.replace(emoji_text, f'<span style="font-size: 1.2em;">{emoji}</span>')
            
            return processed_text
        
        # Add Overview section
        html_content += '<div class="section"><h2>Overview</h2>'
        if 'nutrition_overview' in st.session_state:
            overview_content = st.session_state.nutrition_overview
            # Remove HTML tags but keep the content
            clean_overview = re.sub(r'<.*?>', '', overview_content)
            html_content += convert_markdown_to_html(clean_overview)
        else:
            # Fall back to extracting from the complete plan
            overview_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "introduction", "overview", "caloric", "macronutrient", "recommended"
            ])]
            for section in overview_sections:
                html_content += convert_markdown_to_html(section)
        html_content += '</div>'
        
        # Add Meal Plan section
        html_content += '<div class="section"><h2>Meal Plan</h2>'
        if 'nutrition_meal_plan' in st.session_state:
            meal_plan_content = st.session_state.nutrition_meal_plan
            # Remove HTML tags but keep the content
            clean_meal_plan = re.sub(r'<.*?>', '', meal_plan_content)
            html_content += convert_markdown_to_html(clean_meal_plan)
        else:
            # Fall back to extracting from the complete plan
            meal_plan_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "meal plan", "sample meal", "day 1", "day 2", "day 3"
            ])]
            for section in meal_plan_sections:
                html_content += convert_markdown_to_html(section)
        html_content += '</div>'
        
        # Add Recipes & Tips section
        html_content += '<div class="section"><h2>Recipes & Tips</h2>'
        if 'nutrition_recipes_tips' in st.session_state:
            recipes_tips_content = st.session_state.nutrition_recipes_tips
            # Remove HTML tags but keep the content
            clean_recipes_tips = re.sub(r'<.*?>', '', recipes_tips_content)
            html_content += convert_markdown_to_html(clean_recipes_tips)
        else:
            # Fall back to extracting from the complete plan
            recipe_sections = [s for s in nutrition_plan.split("\n## ") if any(x in s.lower() for x in [
                "recipe", "tips", "avoid", "limit", "portion", "guideline", "stabilize"
            ]) and not any(x in s.lower() for x in ["genetic", "gene", "dna"])]
            for section in recipe_sections:
                html_content += convert_markdown_to_html(section)
        html_content += '</div>'
        
        # Add footer
        html_content += """
            <div class="footer">
                <p>This nutrition plan is personalized based on your health information and is intended as a guide.</p>
                <p>Always consult with healthcare providers before making significant changes to your diet.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    except Exception as e:
        st.error(f"An error occurred while generating the file: {str(e)}")
        # Provide a simpler alternative
        st.info("You can save this page as a PDF using your browser's print function (Ctrl+P or Cmd+P) and selecting 'Save as PDF'.")
        return None

def display_visual_guidance(has_genetic_data=False):
    """
    Display visual guidance for the nutrition plan.
    
    Args:
        has_genetic_data (bool): Whether genetic data is available
    """
    # Get user preferences from health_data if available
    health_data = st.session_state.health_data
    
    # Extract relevant preferences
    food_preferences = health_data.get('food_preferences', [])
    dietary_restrictions_str = health_data.get('dietary_restrictions', '')
    dietary_restrictions = [restriction.strip() for restriction in dietary_restrictions_str.split(',') if restriction.strip()]
    cultural_preferences = health_data.get('cultural_preferences', '')
    
    # Create and display the portion guide
    portion_guide = create_enhanced_portion_guide(cultural_preferences, food_preferences, dietary_restrictions)
    if portion_guide is not None:
        st.pyplot(portion_guide)
    
    # Add educational note about the portion guide
    st.markdown("""
    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: #2e7d32;">How to Use This Portion Guide</h4>
        <ul>
            <li><strong>Half your plate</strong> should be filled with non-starchy vegetables</li>
            <li><strong>One quarter</strong> should contain lean proteins</li>
            <li><strong>One quarter</strong> should have complex carbohydrates</li>
            <li>Include a small serving of fruit and/or dairy on the side</li>
            <li>Add healthy fats in small amounts (olive oil, avocado, nuts)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add genetic-specific note if genetic data is available
    if has_genetic_data and 'genetic_profile' in st.session_state:
        genetic_profile = st.session_state.genetic_profile
        
        # Get carb sensitivity
        carb_sensitivity = genetic_profile.get('carb_metabolism', {}).get('carb_sensitivity', 'normal')
        
        # Get fat sensitivity
        fat_sensitivity = genetic_profile.get('fat_metabolism', {}).get('saturated_fat_sensitivity', 'normal')
        
        # Create genetic-specific recommendations
        carb_advice = "Focus on complex carbohydrates with fiber" if carb_sensitivity == "high" else \
                      "Be mindful of carbohydrate quality and portion size" if carb_sensitivity == "higher" else \
                      "Balance your carbohydrate intake according to the portion guide"
                      
        fat_advice = "Limit saturated fats; choose plant oils & lean proteins" if fat_sensitivity == "high" else \
                     "Moderate your saturated fat intake; focus on unsaturated fats" if fat_sensitivity == "moderate" else \
                     "Include a balanced mix of fats, emphasizing unsaturated sources"
        
        # Display genetic-specific advice
        st.markdown("""
        <div style="background-color: #E8EAF6; padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #3F51B5;">
            <h4 style="color: #3F51B5;">Genetic Optimization Notes</h4>
            <ul>
                <li><strong>Carbohydrates:</strong> """ + carb_advice + """</li>
                <li><strong>Fats:</strong> """ + fat_advice + """</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a separator
    st.markdown("---")
    
    # Display the blood glucose target range visualization
    glucose_guide = create_enhanced_glucose_guide()
    if glucose_guide is not None:
        st.pyplot(glucose_guide)
    
    # Add a separator
    st.markdown("---")
    
    # Display foods to avoid visual
    foods_to_avoid = create_foods_to_avoid_visual(dietary_restrictions)
    if foods_to_avoid is not None:
        st.pyplot(foods_to_avoid)
    
    # Create a container for the "Foods to Limit" section
    limit_container = st.container()
    with limit_container:
        # Add a custom header with red background
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
        
        # Customize based on genetic profile if available
        if has_genetic_data and 'genetic_profile' in st.session_state:
            genetic_profile = st.session_state.genetic_profile
            
            # Add caffeine warning if slow metabolizer
            caffeine_metabolism = genetic_profile.get('caffeine_metabolism', {}).get('caffeine_metabolism', '')
            if caffeine_metabolism in ['slow', 'very slow']:
                limit_foods.append({"icon": "☕", "name": "Caffeine", "reason": f"Your genetic profile indicates {caffeine_metabolism} caffeine metabolism"})
        
        # Display each food item
        for food in limit_foods:
            cols = st.columns([1, 5])
            with cols[0]:
                st.markdown(f"<span style='font-size: 36px;'>{food['icon']}</span>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"**{food['name']}**: {food['reason']}")
    
    # Add a separator
    st.markdown("---")
    
    # Display recommended foods visual
    recommended_foods = create_recommended_foods_visual(cultural_preferences, dietary_restrictions)
    if recommended_foods is not None:
        st.pyplot(recommended_foods)
    
    # Create a container for the "Foods to Choose" section
    choose_container = st.container()
    with choose_container:
        # Add a custom header with green background
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
        
        # Add genetic-specific food recommendations if available
        if has_genetic_data and 'genetic_profile' in st.session_state:
            genetic_profile = st.session_state.genetic_profile
            
            # Add anti-inflammatory foods if needed
            inflammation_response = genetic_profile.get('inflammation_response', {}).get('inflammatory_response', '')
            if inflammation_response in ['elevated', 'moderate']:
                choose_foods.append({"icon": "🐟", "name": "Fatty Fish", "reason": f"Rich in omega-3s to help manage your {inflammation_response} inflammatory response"})
                choose_foods.append({"icon": "🫐", "name": "Berries", "reason": "High in antioxidants that help reduce inflammation"})
            
            # Add folate-rich foods if needed
            folate_processing = genetic_profile.get('vitamin_metabolism', {}).get('folate_processing', '')
            if folate_processing in ['reduced', 'significantly reduced']:
                choose_foods.append({"icon": "🥬", "name": "Leafy Greens", "reason": f"Rich in folate to support your {folate_processing} folate processing ability"})
        
        # Display each food item
        for food in choose_foods:
            cols = st.columns([1, 5])
            with cols[0]:
                st.markdown(f"<span style='font-size: 36px;'>{food['icon']}</span>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"**{food['name']}**: {food['reason']}")
                
    # Add a disclaimer about genetic optimization if applicable
    if has_genetic_data:
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #9C27B0;">
            <h4 style="color: #9C27B0;">Genetic Nutrition Disclaimer</h4>
            <p>The genetic optimization suggestions provided are based on a limited set of genetic markers and current scientific understanding, which continues to evolve. Individual responses may vary, and these recommendations should be considered as complementary to standard diabetes management practices.</p>
            <p>Always consult with healthcare providers before making significant changes to your diet or lifestyle based on genetic information.</p>
        </div>
        """, unsafe_allow_html=True)
