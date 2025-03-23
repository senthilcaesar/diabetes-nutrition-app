"""
Nutrition plan page for the Diabetes Nutrition Plan application.
Displays the generated nutrition plan, genetic optimization, and visual guidance.
"""

import streamlit as st
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
        
        # Add helpful button to navigate to Input Data
        if st.button("Go to Input Data", type="primary", use_container_width=False):
            # Set a navigation flag instead of directly changing radio value
            st.session_state.nav_to_input = True
            st.rerun()
        return
    
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
    
    # Split the nutrition plan into sections
    nutrition_plan = st.session_state.nutrition_plan
    if "\n## " in nutrition_plan:
        sections = nutrition_plan.split("\n## ")
        sections = ["## " + section if i > 0 else section for i, section in enumerate(sections)]
    else:
        sections = nutrition_plan.split("\n### ")
        sections = ["### " + section if i > 0 else section for i, section in enumerate(sections)]
    
    # Extract main sections
    overview_sections = [s for s in sections if any(x in s.lower() for x in [
        "introduction", "overview", "caloric", "macronutrient", "recommended"
    ])]
    
    meal_plan_sections = [s for s in sections if any(x in s.lower() for x in [
        "meal plan", "sample meal", "day 1", "day 2", "day 3"
    ])]
    
    # Look for genetic-specific sections if genetic data is available
    if has_genetic_data:
        genetic_sections = [s for s in sections if any(x in s.lower() for x in [
            "genetic", "gene", "dna", "nutrigenomics", "personalized metabolism"
        ])]
    else:
        genetic_sections = []
    
    recipe_sections = [s for s in sections if any(x in s.lower() for x in [
        "recipe", "tips", "avoid", "limit", "portion", "guideline", "stabilize"
    ]) and not any(x in s.lower() for x in ["genetic", "gene", "dna"])]  # Exclude genetic sections
    
    # Display sections in their respective tabs
    with overview_tab:
        # Display genetic badge at the top if genetic data is used
        if has_genetic_data:
            st.markdown(
                """
                <div style="
                    background-color: #E8EAF6; 
                    border-left: 5px solid #3F51B5;
                    padding: 10px; 
                    border-radius: 4px;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                ">
                    <span style="font-size: 24px; margin-right: 10px;">🧬</span>
                    <span>This nutrition plan has been optimized based on your genetic profile.</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        for section in overview_sections:
            st.markdown(section)
    
    with meal_plan_tab:
        for section in meal_plan_sections:
            st.markdown(section)
    
    # Show genetic optimization tab if genetic data is available
    if has_genetic_data:
        with genetic_tab:
            st.header("Genetic Optimization Strategies")
            
            if genetic_sections:
                for section in genetic_sections:
                    st.markdown(section)
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
            
                st.subheader("Key Recommendations Based on Your Genetic Profile")
                for i, rec in enumerate(genetic_profile.get('key_recommendations', [])):
                    st.markdown(f"- {rec}")
    
    with recipes_tab:
        for section in recipe_sections:
            st.markdown(section)
    
    with visuals_tab:
        if 'visual_guidance' in st.session_state:
            display_visual_guidance(has_genetic_data)
        else:
            st.warning("No visual guidance has been generated yet.")

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