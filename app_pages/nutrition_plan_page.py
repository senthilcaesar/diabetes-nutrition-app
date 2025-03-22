"""
Nutrition plan page for the Diabetes Nutrition Plan application.
Displays the generated nutrition plan and visual guidance.
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
    
    # Display the plan in tabs for better organization
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
    
    recipe_sections = [s for s in sections if any(x in s.lower() for x in [
        "recipe", "tips", "avoid", "limit", "portion", "guideline", "stabilize"
    ])]
    
    # Display sections in their respective tabs
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
            display_visual_guidance()
        else:
            st.warning("No visual guidance has been generated yet.")

def display_visual_guidance():
    """Display visual guidance for the nutrition plan."""
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
        
        # Display each food item
        for food in choose_foods:
            cols = st.columns([1, 5])
            with cols[0]:
                st.markdown(f"<span style='font-size: 36px;'>{food['icon']}</span>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"**{food['name']}**: {food['reason']}")