"""
Genetic LLM integration module for the Diabetes Nutrition Plan application.
Contains functions for integrating genetic data into the nutrition plan.
"""

import json
import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel
from typing import Dict, List, Optional, Any

GEMINI_MODEL = "gemini-1.5-flash"

def format_structured_genetic_nutrition_plan(structured_data):
    """
    Convert the structured genetic nutrition plan data into four separate sections:
    1. Overview - General nutrition plan overview with light genetic context
    2. Meal Plan - Genetically optimized meal plan
    3. Genetic Optimization - Dedicated genetic insights section
    4. Recipes & Tips - Recipe suggestions and blood sugar management tips
    
    Returns:
        tuple: (overview, meal_plan, genetic_section, recipes_tips) sections as formatted text
    """
    try:
        # SECTION 1: OVERVIEW
        overview = ""
        
        # Make sure required elements exist in the structured data
        if not structured_data:
            raise ValueError("Empty structured data")
            
        if "nutritional_overview" not in structured_data:
            raise ValueError("Missing nutritional_overview")
        
        nutritional_overview = structured_data["nutritional_overview"]
        if not isinstance(nutritional_overview, dict):
            raise ValueError("nutritional_overview is not a dictionary")
            
        # Daily Caloric Target with safe fallbacks
        if "daily_caloric_target" in nutritional_overview:
            caloric = nutritional_overview["daily_caloric_target"]
            if isinstance(caloric, dict):
                calories = caloric.get("calories", 2000)
                explanation = caloric.get("explanation", "This caloric target is based on your metabolic needs.")
            else:
                calories = 2000
                explanation = "Unable to retrieve caloric target explanation."
        else:
            calories = 2000
            explanation = "Default caloric target for moderate activity level."
            
        overview += f"### 🔥 Daily Caloric Target: {calories} calories\n\n"
        overview += f"{explanation}\n\n"
        
        # Macronutrient Distribution with visualization-like formatting
        overview += "### 🥗 Macronutrient Distribution\n\n"
        
        # Create a visually appealing macronutrient table
        overview += "| Nutrient | Percentage | Grams |\n"
        overview += "|----------|------------|-------|\n"
        
        # Safely get macronutrient information with fallbacks
        if "macronutrient_distribution" in nutritional_overview and isinstance(nutritional_overview["macronutrient_distribution"], dict):
            macro = nutritional_overview["macronutrient_distribution"]
            
            # Safe getters for each macro
            if "carbohydrates" in macro and isinstance(macro["carbohydrates"], dict):
                carbs = macro["carbohydrates"]
                carb_percent = carbs.get("percentage", 45)
                carb_grams = carbs.get("grams", 225)
                carb_rec = carbs.get("recommendations", "Focus on complex carbohydrates that are digested more slowly.")
            else:
                carb_percent = 45
                carb_grams = 225
                carb_rec = "Focus on complex carbohydrates that are digested more slowly."
                
            if "protein" in macro and isinstance(macro["protein"], dict):
                protein = macro["protein"]
                protein_percent = protein.get("percentage", 25)
                protein_grams = protein.get("grams", 125)
                protein_rec = protein.get("recommendations", "Include lean protein sources with each meal.")
            else:
                protein_percent = 25
                protein_grams = 125
                protein_rec = "Include lean protein sources with each meal."
                
            if "fat" in macro and isinstance(macro["fat"], dict):
                fat = macro["fat"]
                fat_percent = fat.get("percentage", 30)
                fat_grams = fat.get("grams", 67)
                fat_rec = fat.get("recommendations", "Focus on healthy unsaturated fats while limiting saturated fats.")
            else:
                fat_percent = 30
                fat_grams = 67
                fat_rec = "Focus on healthy unsaturated fats while limiting saturated fats."
        else:
            # Default values if no macronutrient_distribution
            carb_percent = 45
            carb_grams = 225
            carb_rec = "Focus on complex carbohydrates with fiber to slow glucose absorption."
            
            protein_percent = 25
            protein_grams = 125
            protein_rec = "Include lean protein sources with each meal."
            
            fat_percent = 30
            fat_grams = 67
            fat_rec = "Focus on healthy unsaturated fats while limiting saturated fats."
        
        # Add table rows with safe values
        overview += f"| **Carbohydrates** | {carb_percent}% | {carb_grams}g |\n"
        overview += f"| **Protein** | {protein_percent}% | {protein_grams}g |\n"
        overview += f"| **Fat** | {fat_percent}% | {fat_grams}g |\n\n"
        
        # Recommendations in styled boxes
        overview += f"**Carbohydrates:** {carb_rec}\n\n"
        overview += f"**Protein:** {protein_rec}\n\n"
        overview += f"**Fat:** {fat_rec}\n\n"
        
        # Meal Structure with clock icon - with safe fallbacks
        overview += "### ⏰ Meal Structure and Timing\n\n"
        
        if "meal_structure" in nutritional_overview and isinstance(nutritional_overview["meal_structure"], dict):
            structure = nutritional_overview["meal_structure"]
            meal_freq = structure.get("meal_frequency", "3-5 meals per day")
            timing_rec = structure.get("timing_recommendations", "Space meals 3-4 hours apart")
            portion_guide = structure.get("portion_guidance", "Use the plate method")
        else:
            meal_freq = "3-5 meals per day"
            timing_rec = "Space meals 3-4 hours apart"
            portion_guide = "Use the plate method"
            
        overview += f"**Meal Frequency:** {meal_freq}\n\n"
        overview += f"**Timing Recommendations:** {timing_rec}\n\n"
        overview += f"**Portion Guidance:** {portion_guide}\n\n"
        
        overview += "---\n\n"
        
        # Recommended Foods section with thumbs up icon
        overview += "### Recommended Foods\n\n"

        # Create a table for foods with headers
        overview += "| Category | Recommended Foods |\n"
        overview += "|----------|-------------------|\n"

        # Safe function to join lists or handle non-list values
        def safe_join(items):
            if isinstance(items, list):
                return ", ".join(items)
            elif isinstance(items, str):
                return items
            else:
                return "No specific recommendations available"

        # Get recommended foods with fallbacks
        if "recommended_foods" in structured_data and isinstance(structured_data["recommended_foods"], dict):
            foods = structured_data["recommended_foods"]
            
            # Safely get each food category with fallbacks
            carbs = foods.get("carbohydrates", ["Whole grains", "Beans", "Lentils", "Sweet potatoes"])
            proteins = foods.get("proteins", ["Lean poultry", "Fish", "Tofu", "Legumes"])
            fats = foods.get("fats", ["Avocados", "Olive oil", "Nuts", "Seeds"])
            vegetables = foods.get("vegetables", ["Leafy greens", "Cruciferous vegetables", "Colorful non-starchy vegetables"])
            fruits = foods.get("fruits", ["Berries", "Apples", "Citrus fruits", "Stone fruits"])
            beverages = foods.get("beverages", ["Water", "Unsweetened tea", "Black coffee"])
        else:
            # Default food lists
            carbs = ["Whole grains", "Beans", "Lentils", "Sweet potatoes"]
            proteins = ["Lean poultry", "Fish", "Tofu", "Legumes"]
            fats = ["Avocados", "Olive oil", "Nuts", "Seeds"]
            vegetables = ["Leafy greens", "Cruciferous vegetables", "Colorful vegetables"]
            fruits = ["Berries", "Apples", "Citrus fruits", "Stone fruits"] 
            beverages = ["Water", "Unsweetened tea", "Black coffee"]

        # Add each category to the table using the safe_join function
        overview += f"| 🌾 **Carbohydrates** | {safe_join(carbs)} |\n"
        overview += f"| 🥩 **Proteins** | {safe_join(proteins)} |\n"
        overview += f"| 🥑 **Fats** | {safe_join(fats)} |\n"
        overview += f"| 🥦 **Vegetables** | {safe_join(vegetables)} |\n"
        overview += f"| 🍎 **Fruits** | {safe_join(fruits)} |\n"
        overview += f"| 🥤 **Beverages** | {safe_join(beverages)} |\n\n"
        
        # SECTION 2: MEAL PLAN
        meal_plan = ""
        
        # Safe day meal getter function
        def get_safe_meal_plan(meal_plans, day_num):
            day_key = f'day{day_num}'
            if not isinstance(meal_plans, dict) or day_key not in meal_plans:
                return {
                    "breakfast": f"Standard balanced breakfast for day {day_num} (data missing)",
                    "lunch": f"Standard balanced lunch for day {day_num} (data missing)",
                    "dinner": f"Standard balanced dinner for day {day_num} (data missing)"
                }
            return meal_plans[day_key]

        if "meal_plans" in structured_data and structured_data["meal_plans"]:
            meal_plans = structured_data["meal_plans"]

            # Create tables for each day
            for day_num in range(1, 4):
                # Get meal plan with fallback
                day_meals = get_safe_meal_plan(meal_plans, day_num)
                
                meal_plan += f"### 🍽️ Day {day_num}\n\n"
                
                # Create table header
                meal_plan += "| Meal | Description |\n"
                meal_plan += "|------|-------------|\n"
                
                # Add each meal with safe fallbacks
                breakfast = day_meals.get('breakfast', f"Balanced breakfast for day {day_num}")
                meal_plan += f"| 🌞 **Breakfast** | {breakfast} |\n"
                
                # Add morning snack if available
                if day_meals.get('morning_snack'):
                    morning_snack = day_meals.get('morning_snack', '')
                    meal_plan += f"| 🥪 **Morning Snack** | {morning_snack} |\n"
                
                # Add lunch
                lunch = day_meals.get('lunch', f"Balanced lunch for day {day_num}")
                meal_plan += f"| 🍲 **Lunch** | {lunch} |\n"
                
                # Add afternoon snack if available
                if day_meals.get('afternoon_snack'):
                    afternoon_snack = day_meals.get('afternoon_snack', '')
                    meal_plan += f"| 🍏 **Afternoon Snack** | {afternoon_snack} |\n"
                
                # Add dinner
                dinner = day_meals.get('dinner', f"Balanced dinner for day {day_num}")
                meal_plan += f"| 🍽️ **Dinner** | {dinner} |\n"
                
                # Add evening snack if available
                if day_meals.get('evening_snack'):
                    evening_snack = day_meals.get('evening_snack', '')
                    meal_plan += f"| 🥛 **Evening Snack** | {evening_snack} |\n"
                
                meal_plan += "\n\n"
        else:
            # Create default meal plan if missing
            meal_plan += "### 🍽️ Day 1\n\n"
            meal_plan += "| Meal | Description |\n"
            meal_plan += "|------|-------------|\n"
            meal_plan += "| 🌞 **Breakfast** | Overnight oats with berries and nuts |\n"
            meal_plan += "| 🥪 **Morning Snack** | Apple with almond butter |\n"
            meal_plan += "| 🍲 **Lunch** | Grilled chicken salad with mixed vegetables |\n"
            meal_plan += "| 🍏 **Afternoon Snack** | Greek yogurt with walnuts |\n"
            meal_plan += "| 🍽️ **Dinner** | Baked fish with roasted vegetables and quinoa |\n\n"
            
            meal_plan += "### 🍽️ Day 2\n\n"
            meal_plan += "| Meal | Description |\n"
            meal_plan += "|------|-------------|\n"
            meal_plan += "| 🌞 **Breakfast** | Vegetable omelet with whole grain toast |\n"
            meal_plan += "| 🥪 **Morning Snack** | Small handful of mixed nuts |\n"
            meal_plan += "| 🍲 **Lunch** | Bean and vegetable soup with a side salad |\n"
            meal_plan += "| 🍏 **Afternoon Snack** | Cottage cheese with berries |\n"
            meal_plan += "| 🍽️ **Dinner** | Turkey stir-fry with vegetables and brown rice |\n\n"
            
            meal_plan += "### 🍽️ Day 3\n\n"
            meal_plan += "| Meal | Description |\n"
            meal_plan += "|------|-------------|\n"
            meal_plan += "| 🌞 **Breakfast** | Greek yogurt parfait with fruit and nuts |\n"
            meal_plan += "| 🥪 **Morning Snack** | Vegetables with hummus |\n"
            meal_plan += "| 🍲 **Lunch** | Lentil salad with roasted vegetables |\n"
            meal_plan += "| 🍏 **Afternoon Snack** | Hard-boiled egg and fruit |\n"
            meal_plan += "| 🍽️ **Dinner** | Grilled chicken with sweet potato and vegetables |\n\n"
        
        # SECTION 3: GENETIC OPTIMIZATION TAB - This section is fully dedicated to genetic insights
        genetic_section = ""
        
        # Add Genetic Optimization Strategies section
        try:
            if "genetic_optimization_strategies" in structured_data:
                genetic = structured_data["genetic_optimization_strategies"]
                
                # Add each genetic strategy with appropriate formatting
                if "carb_metabolism" in genetic:
                    carb_metabolism_text = genetic.get('carb_metabolism', 'Carbohydrate metabolism data not available')
                    genetic_section += f"""
### Carbohydrate Metabolism

<div style="
    background-color: #E8F5E9; 
    border-left: 5px solid #4CAF50;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{carb_metabolism_text}
</div>
"""
                
                if "fat_metabolism" in genetic:
                    fat_metabolism_text = genetic.get('fat_metabolism', 'Fat metabolism data not available')
                    genetic_section += f"""
### Fat Metabolism

<div style="
    background-color: #FFF8E1; 
    border-left: 5px solid #FFC107;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{fat_metabolism_text}
</div>
"""
                
                if "inflammation_response" in genetic:
                    inflammation_text = genetic.get('inflammation_response', 'Inflammation response data not available')
                    genetic_section += f"""
### Inflammation Response

<div style="
    background-color: #FFEBEE; 
    border-left: 5px solid #F44336;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{inflammation_text}
</div>
"""
                
                if "nutrient_processing" in genetic:
                    nutrient_text = genetic.get('nutrient_processing', 'Nutrient processing data not available')
                    genetic_section += f"""
### Nutrient Processing

<div style="
    background-color: #E1F5FE; 
    border-left: 5px solid #03A9F4;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{nutrient_text}
</div>
"""
                
                if "caffeine_metabolism" in genetic:
                    caffeine_text = genetic.get('caffeine_metabolism', 'Caffeine metabolism data not available')
                    genetic_section += f"""
### Caffeine Metabolism

<div style="
    background-color: #F3E5F5; 
    border-left: 5px solid #9C27B0;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{caffeine_text}
</div>
"""
            
            # Add specific foods section based on genetics
            genetic_section += """### Recommended Foods Based on Your Genetic Profile\n\n"""
            
            # Create a list of genetically recommended foods from the structured data
            genetic_section += "| Category | Reason | Foods |\n"
            genetic_section += "|----------|--------|-------|\n"
            
            if "genetic_food_recommendations" in structured_data:
                recommendations = structured_data.get("genetic_food_recommendations", [])
                if isinstance(recommendations, list) and recommendations:
                    for rec in recommendations:
                        if isinstance(rec, dict):
                            category = rec.get('category', 'General')
                            reason = rec.get('reason', 'Genetically optimized')
                            foods = rec.get('foods', 'Various whole foods')
                            genetic_section += f"| **{category}** | {reason} | {foods} |\n"
                else:
                    genetic_section += "| **Omega-3 Sources** | Beneficial for your inflammation profile | Fatty fish, walnuts, flaxseeds |\n"
                    genetic_section += "| **Antioxidant-Rich Foods** | Support your genetic response to oxidative stress | Berries, colorful vegetables, green tea |\n"
                    genetic_section += "| **Fiber Sources** | Optimal for your carbohydrate metabolism | Legumes, whole grains, vegetables |\n"
            else:
                genetic_section += "| **Omega-3 Sources** | Beneficial for your inflammation profile | Fatty fish, walnuts, flaxseeds |\n"
                genetic_section += "| **Antioxidant-Rich Foods** | Support your genetic response to oxidative stress | Berries, colorful vegetables, green tea |\n"
                genetic_section += "| **Fiber Sources** | Optimal for your carbohydrate metabolism | Legumes, whole grains, vegetables |\n"
            
            # Add disclaimer
            genetic_section += """
### Genetic Nutrition Disclaimer

<div style="
    background-color: #F3E5F5; 
    padding: 15px; 
    border-radius: 5px;
    margin: 20px 0;
">
<p>The genetic optimization suggestions provided are based on a limited set of genetic markers and current scientific understanding, which continues to evolve. Individual responses may vary, and these recommendations should be considered as complementary to standard diabetes management practices.</p>

<p>Always consult with healthcare providers before making significant changes to your diet or lifestyle based on genetic information.</p>
</div>
"""
        except Exception as e:
            print(f"Error processing genetic optimization strategies: {e}")
            genetic_section += "### Error: Unable to process genetic optimization strategies.\n\n"
        
        # SECTION 4: RECIPES & TIPS
        recipes_tips = ""
        
        # Simple Recipes with chef hat icon
        if "recipes" in structured_data and structured_data["recipes"]:
            recipes = structured_data["recipes"]
            if isinstance(recipes, list) and len(recipes) > 0:
                for recipe in recipes:
                    if isinstance(recipe, dict):
                        recipes_tips += "<div class='recipe-card'>\n\n"
                        recipes_tips += f"## {recipe.get('name', 'Recipe')}\n\n"
                        recipes_tips += f"**⏱️ Preparation Time:** {recipe.get('prep_time', '30 minutes')}\n\n"
                        recipes_tips += f"**🛒 Ingredients:**\n{recipe.get('ingredients', 'Ingredients not provided')}\n\n"
                        recipes_tips += f"**📝 Instructions:**\n{recipe.get('instructions', 'Instructions not provided')}\n\n"
                        recipes_tips += f"**💪 Nutritional Benefits:** {recipe.get('nutritional_benefits', 'Nutritional information not provided')}\n\n"
                        
                        # Add genetic note if available
                        if 'genetic_note' in recipe:
                            recipes_tips += f"**🧬 Genetic Benefit:** {recipe.get('genetic_note', '')}\n\n"
                            
                        recipes_tips += "</div>\n\n"
                
                recipes_tips += "---\n\n"

        # Foods to Limit section with stop sign icon
        recipes_tips += "# 🛑 Foods to Limit or Avoid\n\n"

        # Create table header
        recipes_tips += "| Food Category | Why to Limit | Better Alternatives |\n"
        recipes_tips += "|---------------|-------------|---------------------|\n"

        # Add each food item as a row in the table - with error handling
        if "foods_to_limit" in structured_data:
            foods_to_limit = structured_data["foods_to_limit"]
            if isinstance(foods_to_limit, list) and len(foods_to_limit) > 0:
                for item in foods_to_limit:
                    if isinstance(item, dict):
                        category = item.get('food_category', 'Processed foods')
                        reason = item.get('reason', 'Can raise blood sugar and inflammation')
                        alternatives = item.get('alternatives', 'Whole food alternatives')
                        recipes_tips += f"| **{category}** | {reason} | {alternatives} |\n"
            else:
                # Fallbacks if empty list or not a list
                recipes_tips += "| **Processed Foods** | High in added sugars and unhealthy fats | Fresh, whole foods |\n"
                recipes_tips += "| **Sugary Beverages** | Can cause blood sugar spikes | Water, herbal tea, infused water |\n"
                recipes_tips += "| **Refined Carbs** | Rapid blood sugar elevation | Whole grains, legumes, vegetables |\n"
        else:
            # Fallbacks if key missing
            recipes_tips += "| **Processed Foods** | High in added sugars and unhealthy fats | Fresh, whole foods |\n"
            recipes_tips += "| **Sugary Beverages** | Can cause blood sugar spikes | Water, herbal tea, infused water |\n"
            recipes_tips += "| **Refined Carbs** | Rapid blood sugar elevation | Whole grains, legumes, vegetables |\n"

        recipes_tips += "---\n\n"
        
        # Blood Sugar Management with chart icon
        if "blood_sugar_management" in structured_data:
            recipes_tips += "# 📈 Blood Sugar Management Strategies\n\n"
            
            bsm = structured_data["blood_sugar_management"]
            if isinstance(bsm, dict):
                # Get values with safe fallbacks
                hypo_prevention = bsm.get('hypoglycemia_prevention', 'Carry fast-acting carbs like glucose tablets or juice for low blood sugar episodes.')
                hyper_management = bsm.get('hyperglycemia_management', 'Stay hydrated, exercise regularly, and monitor blood glucose carefully.')
                meal_timing = bsm.get('meal_timing_strategies', 'Eat meals at consistent times each day to help maintain stable blood sugar levels.')
                snack_recs = bsm.get('snack_recommendations', 'Choose snacks that combine protein and complex carbs for sustained energy.')
                
                recipes_tips += "<div class='management-card'>\n\n"
                recipes_tips += "### 📉 Preventing Low Blood Sugar (Hypoglycemia)\n\n"
                recipes_tips += f"{hypo_prevention}\n\n"
                recipes_tips += "</div>\n\n"
                
                recipes_tips += "<div class='management-card'>\n\n"
                recipes_tips += "### 📈 Managing High Blood Sugar (Hyperglycemia)\n\n"
                recipes_tips += f"{hyper_management}\n\n"
                recipes_tips += "</div>\n\n"
                
                recipes_tips += "<div class='management-card'>\n\n"
                recipes_tips += "### ⏰ Meal Timing Strategies\n\n"
                recipes_tips += f"{meal_timing}\n\n"
                recipes_tips += "</div>\n\n"
                
                recipes_tips += "<div class='management-card'>\n\n"
                recipes_tips += "### 🥕 Smart Snacking\n\n"
                recipes_tips += f"{snack_recs}\n\n"
                recipes_tips += "</div>\n\n"
        else:
            # Provide default blood sugar management section if missing
            recipes_tips += "# 📈 Blood Sugar Management Strategies\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 📉 Preventing Low Blood Sugar (Hypoglycemia)\n\n"
            recipes_tips += "Carry fast-acting carbs like glucose tablets or juice for low blood sugar episodes. Never skip meals and monitor your blood sugar regularly.\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 📈 Managing High Blood Sugar (Hyperglycemia)\n\n"
            recipes_tips += "Stay hydrated, exercise regularly, and follow your medication schedule as prescribed by your healthcare provider.\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### ⏰ Meal Timing Strategies\n\n"
            recipes_tips += "Eat meals at consistent times each day to help maintain stable blood sugar levels.\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 🥕 Smart Snacking\n\n"
            recipes_tips += "Choose snacks that combine protein and complex carbs for sustained energy.\n\n"
            recipes_tips += "</div>\n\n"
        
        return overview, meal_plan, genetic_section, recipes_tips
        
    except Exception as e:
        print(f"Error formatting genetic nutrition plan: {e}")
        # Create fallback sections if formatting fails
        overview = """
        ### 🔥 Daily Caloric Target: 2000 calories

        This is a fallback plan due to formatting errors with the API response.

        ### 🥗 Macronutrient Distribution

        | Nutrient | Percentage | Grams |
        |----------|------------|-------|
        | **Carbohydrates** | 45% | 225g |
        | **Protein** | 25% | 125g |
        | **Fat** | 30% | 67g |

        **Carbohydrates:** Focus on complex carbohydrates like whole grains, legumes, and vegetables.

        **Protein:** Choose lean protein sources such as chicken, fish, tofu, and legumes.

        **Fat:** Emphasize healthy fats from sources like avocados, nuts, seeds, and olive oil.

        ### ⏰ Meal Structure and Timing

        **Meal Frequency:** 3-5 meals per day

        **Timing Recommendations:** Space meals 3-4 hours apart

        **Portion Guidance:** Use the plate method (½ non-starchy vegetables, ¼ protein, ¼ carbohydrates)

        ---

        ### Recommended Foods

        | Category | Recommended Foods |
        |----------|-------------------|
        | 🌾 **Carbohydrates** | Whole grains, beans, lentils, sweet potatoes |
        | 🥩 **Proteins** | Chicken, fish, tofu, eggs, Greek yogurt |
        | 🥑 **Fats** | Avocado, olive oil, nuts, seeds |
        | 🥦 **Vegetables** | Broccoli, spinach, peppers, zucchini |
        | 🍎 **Fruits** | Berries, apples, pears, citrus |
        | 🥤 **Beverages** | Water, unsweetened tea, black coffee |
        """
        
        meal_plan = """
        ## 🍽️ Day 1

        | Meal | Description |
        |------|-------------|
        | 🌞 **Breakfast** | Overnight oats with berries and nuts |
        | 🥪 **Morning Snack** | Apple with almond butter |
        | 🍲 **Lunch** | Grilled chicken salad with mixed vegetables and olive oil dressing |
        | 🍏 **Afternoon Snack** | Greek yogurt with walnuts |
        | 🍽️ **Dinner** | Baked fish with roasted vegetables and quinoa |


        ## 🍽️ Day 2

        | Meal | Description |
        |------|-------------|
        | 🌞 **Breakfast** | Vegetable omelet with whole grain toast |
        | 🥪 **Morning Snack** | Small handful of mixed nuts |
        | 🍲 **Lunch** | Bean and vegetable soup with a side salad |
        | 🍏 **Afternoon Snack** | Cottage cheese with berries |
        | 🍽️ **Dinner** | Turkey stir-fry with vegetables and brown rice |


        ## 🍽️ Day 3

        | Meal | Description |
        |------|-------------|
        | 🌞 **Breakfast** | Greek yogurt parfait with fruit and nuts |
        | 🥪 **Morning Snack** | Vegetables with hummus |
        | 🍲 **Lunch** | Lentil salad with roasted vegetables |
        | 🍏 **Afternoon Snack** | Hard-boiled egg and fruit |
        | 🍽️ **Dinner** | Grilled chicken with sweet potato and steamed vegetables |
        """
        
        genetic_section = """
        ### Carbohydrate Metabolism

        <div style="
            background-color: #E8F5E9; 
            border-left: 5px solid #4CAF50;
            padding: 15px; 
            border-radius: 5px;
            margin-bottom: 20px;
        ">
        Based on your genetic profile, you may have a moderate sensitivity to carbohydrates. This suggests your body processes carbohydrates at an average rate. Focus on complex carbohydrates with fiber to slow glucose absorption.
        </div>

        ### Fat Metabolism

        <div style="
            background-color: #FFF8E1; 
            border-left: 5px solid #FFC107;
            padding: 15px; 
            border-radius: 5px;
            margin-bottom: 20px;
        ">
        Your genetic profile suggests a typical response to dietary fats. Focus on unsaturated fats while limiting saturated fats to support healthy cholesterol levels.
        </div>

        ### Inflammation Response

        <div style="
            background-color: #FFEBEE; 
            border-left: 5px solid #F44336;
            padding: 15px; 
            border-radius: 5px;
            margin-bottom: 20px;
        ">
        Your genetic variants suggest a standard inflammatory response. Include anti-inflammatory foods like fatty fish, olive oil, and leafy greens regularly in your diet.
        </div>

        ### Recommended Foods Based on Your Genetic Profile

        | Category | Reason | Foods |
        |----------|--------|-------|
        | **Omega-3 Sources** | Beneficial for your inflammation profile | Fatty fish, walnuts, flaxseeds |
        | **Antioxidant-Rich Foods** | Support your genetic response to oxidative stress | Berries, colorful vegetables, green tea |
        | **Fiber Sources** | Optimal for your carbohydrate metabolism | Legumes, whole grains, vegetables |

        ### Genetic Nutrition Disclaimer

        <div style="
            background-color: #F3E5F5; 
            padding: 15px; 
            border-radius: 5px;
            margin: 20px 0;
        ">
        <p>The genetic optimization suggestions provided are based on a limited set of genetic markers and current scientific understanding, which continues to evolve. Individual responses may vary, and these recommendations should be considered as complementary to standard diabetes management practices.</p>

        <p>Always consult with healthcare providers before making significant changes to your diet or lifestyle based on genetic information.</p>
        </div>
        """
        
        recipes_tips = """
        # 🛑 Foods to Limit or Avoid

        | Food Category | Why to Limit | Better Alternatives |
        |---------------|-------------|---------------------|
        | **Sugary Foods** | Can cause blood sugar spikes | Fresh fruit, berries |
        | **Refined Carbs** | Rapid blood sugar elevation | Whole grains, legumes |
        | **Fried Foods** | High in unhealthy fats | Baked, grilled, or steamed options |

        ---

        # 📈 Blood Sugar Management Strategies

        <div class='management-card'>

        ### 📉 Preventing Low Blood Sugar (Hypoglycemia)

        Carry fast-acting carbs like glucose tablets. Never skip meals. Monitor blood sugar regularly.

        </div>

        <div class='management-card'>

        ### 📈 Managing High Blood Sugar (Hyperglycemia)

        Stay hydrated, exercise regularly, and follow your medication schedule as prescribed.

        </div>

        <div class='management-card'>

        ### ⏰ Meal Timing Strategies

        Eat meals at consistent times each day to help maintain stable blood sugar levels.

        </div>

        <div class='management-card'>

        ### 🥕 Smart Snacking

        Choose snacks that combine protein and complex carbs for sustained energy.

        </div>
        """
    
        return overview, meal_plan, genetic_section, recipes_tips

def create_genetic_nutrition_plan_tools():
    """
    Create a structured tools schema for generating genetically optimized nutrition plans.
    
    Returns:
        list: A list containing the function schema for genetic nutrition plan
    """
    tools = [
        {
            "function_declarations": [
                {
                    "name": "generate_structured_genetic_nutrition_plan",
                    "description": "Generate a structured nutrition plan for a diabetes patient that incorporates genetic insights alongside health and socioeconomic data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "introduction": {
                                "type": "string",
                                "description": "A personalized introduction to the nutrition plan that addresses the individual's specific situation including genetic factors."
                            },
                            "nutritional_overview": {
                                "type": "object",
                                "description": "Overview of the nutritional approach and guidelines with genetic optimization",
                                "properties": {
                                    "daily_caloric_target": {
                                        "type": "object",
                                        "properties": {
                                            "calories": {"type": "number"},
                                            "explanation": {"type": "string"}
                                        }
                                    },
                                    "macronutrient_distribution": {
                                        "type": "object",
                                        "properties": {
                                            "carbohydrates": {
                                                "type": "object",
                                                "properties": {
                                                    "percentage": {"type": "number"},
                                                    "grams": {"type": "number"},
                                                    "recommendations": {"type": "string"}
                                                }
                                            },
                                            "protein": {
                                                "type": "object",
                                                "properties": {
                                                    "percentage": {"type": "number"},
                                                    "grams": {"type": "number"},
                                                    "recommendations": {"type": "string"}
                                                }
                                            },
                                            "fat": {
                                                "type": "object",
                                                "properties": {
                                                    "percentage": {"type": "number"},
                                                    "grams": {"type": "number"},
                                                    "recommendations": {"type": "string"}
                                                }
                                            }
                                        }
                                    },
                                    "meal_structure": {
                                        "type": "object",
                                        "properties": {
                                            "meal_frequency": {"type": "string"},
                                            "timing_recommendations": {"type": "string"},
                                            "portion_guidance": {"type": "string"}
                                        }
                                    }
                                }
                            },
                            "genetic_optimization_strategies": {
                                "type": "object",
                                "description": "Specific nutrition strategies based on genetic profile",
                                "properties": {
                                    "carb_metabolism": {"type": "string"},
                                    "fat_metabolism": {"type": "string"},
                                    "inflammation_response": {"type": "string"},
                                    "nutrient_processing": {"type": "string"},
                                    "caffeine_metabolism": {"type": "string"}
                                }
                            },
                            "recommended_foods": {
                                "type": "object",
                                "description": "Foods that are recommended based on both diabetes management and genetic profile",
                                "properties": {
                                    "carbohydrates": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "proteins": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "fats": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "vegetables": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "fruits": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "beverages": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            },
                            "foods_to_limit": {
                                "type": "array",
                                "description": "Foods that should be limited or avoided based on both diabetes management and genetic factors",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "food_category": {"type": "string"},
                                        "reason": {"type": "string"},
                                        "alternatives": {"type": "string"},
                                        "genetic_context": {"type": "string"}
                                    }
                                }
                            },
                            "meal_plans": {
                                "type": "object",
                                "description": "Sample genetically-optimized meal plans for different days",
                                "properties": {
                                    "day1": {
                                        "type": "object",
                                        "properties": {
                                            "breakfast": {"type": "string"},
                                            "morning_snack": {"type": "string"},
                                            "lunch": {"type": "string"},
                                            "afternoon_snack": {"type": "string"},
                                            "dinner": {"type": "string"},
                                            "evening_snack": {"type": "string"}
                                        }
                                    },
                                    "day2": {
                                        "type": "object",
                                        "properties": {
                                            "breakfast": {"type": "string"},
                                            "morning_snack": {"type": "string"},
                                            "lunch": {"type": "string"},
                                            "afternoon_snack": {"type": "string"},
                                            "dinner": {"type": "string"},
                                            "evening_snack": {"type": "string"}
                                        }
                                    },
                                    "day3": {
                                        "type": "object",
                                        "properties": {
                                            "breakfast": {"type": "string"},
                                            "morning_snack": {"type": "string"},
                                            "lunch": {"type": "string"},
                                            "afternoon_snack": {"type": "string"},
                                            "dinner": {"type": "string"},
                                            "evening_snack": {"type": "string"}
                                        }
                                    }
                                }
                            },
                            "recipes": {
                                "type": "array",
                                "description": "Simple recipes tailored to the individual's preferences, resources, and genetic profile",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "ingredients": {"type": "string"},
                                        "instructions": {"type": "string"},
                                        "prep_time": {"type": "string"},
                                        "nutritional_benefits": {"type": "string"},
                                        "genetic_note": {"type": "string"}
                                    }
                                }
                            },
                            "blood_sugar_management": {
                                "type": "object",
                                "description": "Strategies for managing blood sugar through nutrition with genetic optimization",
                                "properties": {
                                    "hypoglycemia_prevention": {"type": "string"},
                                    "hyperglycemia_management": {"type": "string"},
                                    "meal_timing_strategies": {"type": "string"},
                                    "snack_recommendations": {"type": "string"},
                                    "genetic_considerations": {"type": "string"}
                                }
                            },
                            "genetic_disclaimer": {
                                "type": "string",
                                "description": "Disclaimer about genetic-based nutrition recommendations and their limitations"
                            }
                        },
                        "required": ["introduction", "nutritional_overview", "genetic_optimization_strategies", "recommended_foods", "foods_to_limit", "meal_plans"]
                    }
                }
            ]
        }
    ]
    
    return tools

def generate_genetic_enhanced_nutrition_plan(user_data, genetic_profile):
    """
    Generate a nutrition plan that incorporates genetic insights.
    
    Args:
        user_data (dict): Dictionary containing user health and socioeconomic data
        genetic_profile (dict): Dictionary containing genetic nutrition profile
        
    Returns:
        tuple: (nutrition_plan, overview, meal_plan, genetic_section, recipes_tips) - complete plan and individual sections
    """
    prompt = create_genetic_nutrition_plan_prompt(user_data, genetic_profile)
    
    # Initialize Gemini
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Get the tools schema
    tools = create_genetic_nutrition_plan_tools()
    
    # Create model instance
    model = GenerativeModel(GEMINI_MODEL)
    
    # Generate response with function calling
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": "You are a medical nutrition specialist with expertise in both diabetes management and nutrigenomics. Create a personalized nutrition plan that integrates both health data and genetic insights."
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        generation_config={"temperature": 0.3},
        tools=tools,
        tool_config={"function_calling_config": {"mode": "any"}}
    )
    
    # Check if function calling was used
    try:
        # Extract the structured response from function call
        if hasattr(response.candidates[0].content, 'parts') and hasattr(response.candidates[0].content.parts[0], 'function_call'):
            function_call = response.candidates[0].content.parts[0].function_call
            # Print for debugging
            print(f"Function call response: {function_call}")
            print(f"Args type: {type(function_call.args)}")
            print(f"Args: {function_call.args}")
            
            # Get the args safely - Gemini 1.5 API response handling
            try:
                if hasattr(function_call.args, 'to_dict'):
                    structured_plan = function_call.args.to_dict()
                elif hasattr(function_call.args, '_asdict'):
                    structured_plan = function_call.args._asdict()
                elif hasattr(function_call.args, '__dict__'):
                    structured_plan = function_call.args.__dict__
                elif hasattr(function_call.args, '_pb'):
                    # Extract from _pb attribute which is a MessageMapContainer
                    pb_obj = function_call.args._pb
                    
                    # Try to extract data from _pb
                    try:
                        # Use items() method if available
                        extracted_data = {}
                        for key, value in pb_obj.items():
                            # Extract the actual value from the structure
                            str_value = str(value)
                            
                            # Parse number and string values
                            if 'number_value:' in str_value:
                                # Extract numeric value
                                num_str = str_value.split('number_value:')[1].strip()
                                try:
                                    # Try to convert to int first, then float
                                    extracted_data[key] = int(num_str)
                                except ValueError:
                                    try:
                                        extracted_data[key] = float(num_str)
                                    except ValueError:
                                        extracted_data[key] = num_str
                            elif 'string_value:' in str_value:
                                # Extract string value, removing quotes
                                str_content = str_value.split('string_value:')[1].strip()
                                extracted_data[key] = str_content.strip('"')
                            else:
                                # For other types, store string representation
                                extracted_data[key] = str_value
                        
                        # Set up default values
                        introduction = extracted_data.get("introduction", "Personalized Nutrition Plan with Genetic Insights")
                        
                        # Set up nutritional overview with default values
                        nutritional_overview = {
                            "daily_caloric_target": {"calories": 2000, "explanation": "Default caloric target for moderate activity level."},
                            "macronutrient_distribution": {
                                "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "Focus on complex carbs"},
                                "protein": {"percentage": 25, "grams": 125, "recommendations": "Choose lean proteins"},
                                "fat": {"percentage": 30, "grams": 67, "recommendations": "Focus on healthy fats"}
                            },
                            "meal_structure": {
                                "meal_frequency": "3-5 meals per day",
                                "timing_recommendations": "Space meals 3-4 hours apart",
                                "portion_guidance": "Use the plate method"
                            }
                        }
                        
                        # Set default genetic strategies
                        genetic_strategies = {
                            "carb_metabolism": "Based on your genetic profile, focus on complex carbohydrates with fiber.",
                            "fat_metabolism": "Your genetic profile suggests focusing on healthy unsaturated fats.",
                            "inflammation_response": "Consider adding anti-inflammatory foods to your diet based on your genetic profile.",
                            "nutrient_processing": "Your genetic profile indicates potential need for specific nutrients.",
                            "caffeine_metabolism": "Based on your genetics, moderate caffeine consumption is recommended."
                        }
                        
                        # Try to extract genetic strategies if available
                        if "genetic_optimization_strategies" in extracted_data:
                            genetic_str = str(extracted_data["genetic_optimization_strategies"])
                            
                            # Extract carb metabolism if available
                            if "carb_metabolism" in genetic_str:
                                carb_parts = genetic_str.split("carb_metabolism")
                                if len(carb_parts) > 1:
                                    carb_value = carb_parts[1].split(",")[0].strip(': "\'')
                                    genetic_strategies["carb_metabolism"] = carb_value
                            
                            # Extract fat metabolism if available
                            if "fat_metabolism" in genetic_str:
                                fat_parts = genetic_str.split("fat_metabolism")
                                if len(fat_parts) > 1:
                                    fat_value = fat_parts[1].split(",")[0].strip(': "\'')
                                    genetic_strategies["fat_metabolism"] = fat_value
                        
                        # Build structured plan
                        structured_plan = {
                            "introduction": introduction,
                            "nutritional_overview": nutritional_overview,
                            "genetic_optimization_strategies": genetic_strategies,
                            "recommended_foods": extracted_data.get("recommended_foods", {
                                "carbohydrates": ["Whole grains", "Legumes", "Vegetables"],
                                "proteins": ["Lean meats", "Fish", "Legumes"],
                                "fats": ["Avocado", "Nuts", "Olive oil"],
                                "vegetables": ["Leafy greens", "Cruciferous vegetables"],
                                "fruits": ["Berries", "Apples", "Citrus"],
                                "beverages": ["Water", "Herbal tea", "Black coffee"]
                            }),
                            "foods_to_limit": extracted_data.get("foods_to_limit", [
                                {"food_category": "Processed Foods", "reason": "High in added sugars", "alternatives": "Whole foods"}
                            ]),
                            "meal_plans": extracted_data.get("meal_plans", {
                                "day1": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                                "day2": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                                "day3": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"}
                            }),
                            "genetic_food_recommendations": extracted_data.get("genetic_food_recommendations", [
                                {"category": "Omega-3 Rich Foods", "reason": "Beneficial for your genetic profile", "foods": "Fatty fish, walnuts, flaxseeds"}
                            ])
                        }
                    except Exception as e:
                        print(f"Error iterating through _pb: {e}")
                        
                        # Fallback to default structured plan
                        structured_plan = {
                            "introduction": "Personalized Nutrition Plan with Genetic Insights",
                            "nutritional_overview": {
                                "daily_caloric_target": {"calories": 2000, "explanation": "Based on your profile and genetic factors."},
                                "macronutrient_distribution": {
                                    "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "Focus on complex carbohydrates with fiber."},
                                    "protein": {"percentage": 25, "grams": 125, "recommendations": "Choose lean protein sources."},
                                    "fat": {"percentage": 30, "grams": 67, "recommendations": "Emphasize healthy unsaturated fats."}
                                },
                                "meal_structure": {
                                    "meal_frequency": "3-5 meals per day",
                                    "timing_recommendations": "Space meals 3-4 hours apart to help maintain stable blood sugar",
                                    "portion_guidance": "Use the plate method: ½ non-starchy vegetables, ¼ protein, ¼ carbohydrates"
                                }
                            },
                            "genetic_optimization_strategies": {
                                "carb_metabolism": "Based on your genetic profile, focus on complex carbohydrates with fiber.",
                                "fat_metabolism": "Your genetic profile suggests focusing on healthy unsaturated fats.",
                                "inflammation_response": "Consider adding anti-inflammatory foods to your diet based on your genetic profile.",
                                "nutrient_processing": "Your genetic profile indicates potential need for specific nutrients.",
                                "caffeine_metabolism": "Based on your genetics, moderate caffeine consumption is recommended."
                            },
                            "recommended_foods": {
                                "carbohydrates": ["Whole grains (brown rice, quinoa, oats)", "Legumes (beans, lentils)", "Sweet potatoes"],
                                "proteins": ["Fatty fish like salmon", "Lean poultry", "Tofu and tempeh", "Legumes"],
                                "fats": ["Avocados", "Nuts and seeds", "Olive oil", "Fatty fish"],
                                "vegetables": ["Leafy greens", "Broccoli", "Peppers", "Cauliflower"],
                                "fruits": ["Berries", "Apples", "Citrus fruits", "Cherries"],
                                "beverages": ["Water", "Green tea", "Herbal tea"]
                            },
                            "foods_to_limit": [
                                {"food_category": "Sugary Foods", "reason": "Can cause blood sugar spikes and inflammation", "alternatives": "Fresh berries, apple with almond butter"},
                                {"food_category": "Refined Carbohydrates", "reason": "Your genetic profile shows sensitivity to refined carbs", "alternatives": "Whole grains, sweet potatoes"}
                            ],
                            "meal_plans": {
                                "day1": {
                                    "breakfast": "Overnight oats with berries, nuts, and cinnamon",
                                    "lunch": "Grilled salmon salad with olive oil dressing",
                                    "dinner": "Turkey and vegetable stir-fry with brown rice"
                                },
                                "day2": {
                                    "breakfast": "Veggie omelet with avocado and whole grain toast",
                                    "lunch": "Lentil soup with leafy green salad",
                                    "dinner": "Baked cod with roasted vegetables and quinoa"
                                },
                                "day3": {
                                    "breakfast": "Greek yogurt with berries, nuts, and seeds",
                                    "lunch": "Chicken and vegetable wrap with hummus",
                                    "dinner": "Bean and vegetable chili with small side salad"
                                }
                            },
                            "genetic_food_recommendations": [
                                {"category": "Omega-3 Rich Foods", "reason": "Beneficial for your genetic inflammation profile", "foods": "Fatty fish, walnuts, flaxseeds, chia seeds"},
                                {"category": "Antioxidant-Rich Foods", "reason": "Support your genetic response to oxidative stress", "foods": "Berries, dark leafy greens, colorful vegetables"}
                            ]
                        }
                else:
                    # Try accessing individual properties directly
                    introduction = getattr(function_call.args, "introduction", "Personalized Nutrition Plan with Genetic Insights")
                    
                    # Extract nutritional overview with careful property access
                    if hasattr(function_call.args, "nutritional_overview"):
                        nutritional_overview = function_call.args.nutritional_overview
                    else:
                        nutritional_overview = {
                            "daily_caloric_target": {"calories": 2000, "explanation": "Default values used"},
                            "macronutrient_distribution": {
                                "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "Focus on complex carbs"},
                                "protein": {"percentage": 25, "grams": 125, "recommendations": "Choose lean proteins"},
                                "fat": {"percentage": 30, "grams": 67, "recommendations": "Focus on healthy fats"}
                            },
                            "meal_structure": {
                                "meal_frequency": "3-5 meals per day",
                                "timing_recommendations": "Space meals 3-4 hours apart",
                                "portion_guidance": "Use the plate method"
                            }
                        }
                    
                    # Extract genetic optimization strategies
                    if hasattr(function_call.args, "genetic_optimization_strategies"):
                        genetic_strategies = function_call.args.genetic_optimization_strategies
                    else:
                        genetic_strategies = {
                            "carb_metabolism": "Based on your genetic profile, focus on complex carbohydrates with fiber.",
                            "fat_metabolism": "Your genetic profile suggests focusing on healthy unsaturated fats.",
                            "inflammation_response": "Consider adding anti-inflammatory foods to your diet based on your genetic profile.",
                            "nutrient_processing": "Your genetic profile indicates potential need for specific nutrients.",
                            "caffeine_metabolism": "Based on your genetics, moderate caffeine consumption is recommended."
                        }
                    
                    # Build structured plan from individual properties
                    structured_plan = {
                        "introduction": introduction,
                        "nutritional_overview": nutritional_overview,
                        "genetic_optimization_strategies": genetic_strategies,
                        "recommended_foods": getattr(function_call.args, "recommended_foods", {
                            "carbohydrates": ["Whole grains", "Legumes", "Vegetables"],
                            "proteins": ["Lean meats", "Fish", "Legumes"],
                            "fats": ["Avocado", "Nuts", "Olive oil"],
                            "vegetables": ["Leafy greens", "Cruciferous vegetables"],
                            "fruits": ["Berries", "Apples", "Citrus"],
                            "beverages": ["Water", "Herbal tea", "Black coffee"]
                        }),
                        "foods_to_limit": getattr(function_call.args, "foods_to_limit", [
                            {"food_category": "Processed Foods", "reason": "High in added sugars", "alternatives": "Whole foods"}
                        ]),
                        "meal_plans": getattr(function_call.args, "meal_plans", {
                            "day1": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                            "day2": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                            "day3": {"breakfast": "Genetically optimized breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"}
                        }),
                        "genetic_food_recommendations": getattr(function_call.args, "genetic_food_recommendations", [
                            {"category": "Omega-3 Rich Foods", "reason": "Beneficial for your genetic profile", "foods": "Fatty fish, walnuts, flaxseeds"}
                        ])
                    }
            except Exception as e:
                print(f"Error extracting args with attribute access: {e}")
                # Fallback to a basic structure if all methods fail
                structured_plan = {
                    "introduction": "Error parsing API response",
                    "nutritional_overview": {
                        "daily_caloric_target": {"calories": 2000, "explanation": "Error parsing API response"},
                        "macronutrient_distribution": {
                            "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "API error"},
                            "protein": {"percentage": 25, "grams": 125, "recommendations": "API error"},
                            "fat": {"percentage": 30, "grams": 67, "recommendations": "API error"}
                        },
                        "meal_structure": {
                            "meal_frequency": "Error parsing response",
                            "timing_recommendations": "Error parsing response",
                            "portion_guidance": "Error parsing response"
                        }
                    },
                    "genetic_optimization_strategies": {
                        "carb_metabolism": "Error parsing response",
                        "fat_metabolism": "Error parsing response",
                        "inflammation_response": "Error parsing response",
                        "nutrient_processing": "Error parsing response",
                        "caffeine_metabolism": "Error parsing response"
                    },
                    "recommended_foods": {
                        "carbohydrates": ["Error processing response"],
                        "proteins": ["Error processing response"],
                        "fats": ["Error processing response"],
                        "vegetables": ["Error processing response"],
                        "fruits": ["Error processing response"],
                        "beverages": ["Error processing response"]
                    },
                    "foods_to_limit": [{"food_category": "Error", "reason": "Error", "alternatives": "Error"}],
                    "meal_plans": {
                        "day1": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"},
                        "day2": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"},
                        "day3": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"}
                    }
                }
        else:
            # If no function call, process as regular text response
            print("No function call found in response. Full response:")
            print(response)
            # Try to extract any usable text
            try:
                text_response = response.text
                print(f"Text response: {text_response}")
                # Create a simple structured response
                structured_plan = {
                    "introduction": "Model did not use function calling - see raw response below",
                    "nutritional_overview": {
                        "daily_caloric_target": {"calories": 2000, "explanation": "Model did not use function calling - see raw response below"},
                        "macronutrient_distribution": {
                            "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "See raw response"},
                            "protein": {"percentage": 25, "grams": 125, "recommendations": "See raw response"},
                            "fat": {"percentage": 30, "grams": 67, "recommendations": "See raw response"}
                        },
                        "meal_structure": {
                            "meal_frequency": "3-5 meals per day",
                            "timing_recommendations": "See raw response",
                            "portion_guidance": "See raw response"
                        }
                    },
                    "genetic_optimization_strategies": {
                        "carb_metabolism": "See raw model response",
                        "fat_metabolism": "See raw model response",
                        "inflammation_response": "See raw model response",
                        "nutrient_processing": "See raw model response",
                        "caffeine_metabolism": "See raw model response"
                    },
                    "recommended_foods": {
                        "carbohydrates": ["See raw response"],
                        "proteins": ["See raw response"],
                        "fats": ["See raw response"],
                        "vegetables": ["See raw response"],
                        "fruits": ["See raw response"],
                        "beverages": ["See raw response"]
                    },
                    "foods_to_limit": [{"food_category": "See raw response", "reason": "Raw response:", "alternatives": text_response[:200] + "..."}],
                    "meal_plans": {
                        "day1": {"breakfast": "See raw response", "lunch": "See raw response", "dinner": "See raw response"},
                        "day2": {"breakfast": "See raw response", "lunch": "See raw response", "dinner": "See raw response"},
                        "day3": {"breakfast": "See raw response", "lunch": "See raw response", "dinner": "See raw response"}
                    }
                }
            except Exception as e:
                print(f"Error processing text response: {e}")
                raise
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Response structure: {response}")
        # Create a minimal fallback structure
        structured_plan = {
            "introduction": f"Error: {str(e)}",
            "nutritional_overview": {
                "daily_caloric_target": {"calories": 2000, "explanation": f"Error: {str(e)}"},
                "macronutrient_distribution": {
                    "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "Error in response processing"},
                    "protein": {"percentage": 25, "grams": 125, "recommendations": "Error in response processing"},
                    "fat": {"percentage": 30, "grams": 67, "recommendations": "Error in response processing"}
                },
                "meal_structure": {
                    "meal_frequency": "Error in response processing",
                    "timing_recommendations": "Error in response processing",
                    "portion_guidance": "Error in response processing"
                }
            },
            "genetic_optimization_strategies": {
                "carb_metabolism": "Error in response processing",
                "fat_metabolism": "Error in response processing",
                "inflammation_response": "Error in response processing",
                "nutrient_processing": "Error in response processing",
                "caffeine_metabolism": "Error in response processing"
            },
            "recommended_foods": {
                "carbohydrates": ["Error in response processing"],
                "proteins": ["Error in response processing"],
                "fats": ["Error in response processing"],
                "vegetables": ["Error in response processing"],
                "fruits": ["Error in response processing"],
                "beverages": ["Error in response processing"]
            },
            "foods_to_limit": [{"food_category": "Error", "reason": "Error in response processing", "alternatives": "Error"}],
            "meal_plans": {
                "day1": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"},
                "day2": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"},
                "day3": {"breakfast": "Error", "lunch": "Error", "dinner": "Error"}
            }
        }
    
    # Format the structured data into separate sections
    overview, meal_plan, genetic_section, recipes_tips = format_structured_genetic_nutrition_plan(structured_plan)
    
    # Also create a complete plan by combining all sections (for backward compatibility)
    nutrition_plan = overview + "\n" + meal_plan + "\n" + genetic_section + "\n" + recipes_tips
    
    # Store all sections in session state
    st.session_state.nutrition_plan = nutrition_plan
    st.session_state.nutrition_overview = overview
    st.session_state.nutrition_meal_plan = meal_plan
    st.session_state.nutrition_genetic_section = genetic_section
    st.session_state.nutrition_recipes_tips = recipes_tips
    
    return nutrition_plan, overview, meal_plan, genetic_section, recipes_tips

def create_genetic_nutrition_plan_prompt(user_data: Dict, genetic_profile: Dict) -> str:
    """
    Create a prompt for generating a nutrition plan with genetic insights.
    
    Args:
        user_data (Dict): Dictionary containing user health and socioeconomic data
        genetic_profile (Dict): Dictionary containing genetic nutrition profile
        
    Returns:
        str: Generated prompt
    """
    # Extract standard user data
    diabetes_type = user_data.get('diabetes_type', 'Type 2')
    format_guidance = user_data.get('format_guidance', 'balanced text and visuals')
    plan_complexity = user_data.get('plan_complexity', 'moderate')
    cultural_foods = user_data.get('cultural_foods', 'No specific cultural preferences')
    literacy_level = user_data.get('literacy_level', 'moderate')
    income_level = user_data.get('income_level', 'medium')
    grocery_budget = user_data.get('grocery_budget', 'moderate')
    local_foods = user_data.get('local_food_availability', 'moderate')
    
    # Standard health information
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
    
    # Socioeconomic information
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
    
    # Format genetic insights
    genetic_info = """
    ## Genetic Insights
    """
    
    # Add carbohydrate metabolism insights
    carb_metabolism = genetic_profile.get("carb_metabolism", {})
    genetic_info += f"""
    ### Carbohydrate Metabolism
    - Carbohydrate Sensitivity: {carb_metabolism.get('carb_sensitivity', 'normal')}
    - Explanation: {carb_metabolism.get('explanation', '')}
    - Key Recommendations:
    """
    for rec in carb_metabolism.get('recommendations', []):
        genetic_info += f"  - {rec}\n"
    
    # Add fat metabolism insights
    fat_metabolism = genetic_profile.get("fat_metabolism", {})
    genetic_info += f"""
    ### Fat Metabolism
    - Saturated Fat Sensitivity: {fat_metabolism.get('saturated_fat_sensitivity', 'normal')}
    - Explanation: {fat_metabolism.get('explanation', '')}
    - Key Recommendations:
    """
    for rec in fat_metabolism.get('recommendations', []):
        genetic_info += f"  - {rec}\n"
    
    # Add vitamin metabolism insights
    vitamin_metabolism = genetic_profile.get("vitamin_metabolism", {})
    genetic_info += f"""
    ### Vitamin Metabolism
    - Folate Processing: {vitamin_metabolism.get('folate_processing', 'normal')}
    - Explanation: {vitamin_metabolism.get('explanation', '')}
    - Key Recommendations:
    """
    for rec in vitamin_metabolism.get('recommendations', []):
        genetic_info += f"  - {rec}\n"
    
    # Add inflammation response insights
    inflammation_response = genetic_profile.get("inflammation_response", {})
    genetic_info += f"""
    ### Inflammation Response
    - Inflammatory Response: {inflammation_response.get('inflammatory_response', 'normal')}
    - Explanation: {inflammation_response.get('explanation', '')}
    - Key Recommendations:
    """
    for rec in inflammation_response.get('recommendations', []):
        genetic_info += f"  - {rec}\n"
    
    # Add caffeine metabolism insights
    caffeine_metabolism = genetic_profile.get("caffeine_metabolism", {})
    genetic_info += f"""
    ### Caffeine Metabolism
    - Caffeine Processing: {caffeine_metabolism.get('caffeine_metabolism', 'normal')}
    - Explanation: {caffeine_metabolism.get('explanation', '')}
    - Key Recommendations:
    """
    for rec in caffeine_metabolism.get('recommendations', []):
        genetic_info += f"  - {rec}\n"
    
    # Add overall genetic summary
    genetic_info += f"""
    ### Overall Genetic Summary
    {genetic_profile.get('overall_summary', '')}
    
    Key Genetic-Based Recommendations:
    """
    for rec in genetic_profile.get('key_recommendations', []):
        genetic_info += f"- {rec}\n"
    
    # Build the complete prompt
    prompt = f"""
    Create a comprehensive, personalized nutrition plan for an individual with {diabetes_type} diabetes based on both their health/socioeconomic profile AND their genetic insights:
    
    {health_info}
    
    {socio_info}
    
    {genetic_info}
    
    ## Plan Specifications
    Please create a genetically-optimized nutrition plan that includes:
    
    1. Daily caloric target and macronutrient distribution (carbs, protein, fat) tailored to their genetic profile
    2. Recommended meal structure (timing and composition) based on metabolic genetic factors
    3. A sample 3-day meal plan with specific foods that align with their genetic predispositions
    4. Simple recipe ideas that incorporate the genetic insights
    5. Guidance on foods to prioritize and avoid based on their genetic profile
    6. Specific genetic optimization strategies for blood sugar management
    
    The plan should:
    - Integrate genetic insights with diabetes management best practices
    - Be culturally appropriate and incorporate local food options
    - Remain affordable within the specified budget
    - Be easy to understand with the specified literacy level in mind
    - Be practical considering the individual's living conditions and cooking facilities
    
    {'' if plan_complexity != 'simple' else 'Make the plan extremely simple, using basic language, visual cues, and minimal text. Focus on practical, actionable guidance rather than detailed explanations.'}
    
    {'' if plan_complexity != 'advanced' else 'Include more detailed nutritional information, rationale for recommendations, and guidance on adapting the plan as needed.'}
    
    {'' if 'visual' not in format_guidance else 'Design the plan to be highly visual with food images, simple icons, and minimal text. Use color coding to indicate foods that are encouraged (green), to be consumed in moderation (yellow), or to be limited/avoided (red).'}
    
    Please clearly incorporate the genetic insights throughout the nutrition plan, making it evident how the recommendations are personalized based on both diabetes management principles AND genetic factors.
    
    Return the plan in a well-formatted structure with clear sections, including a specific section called "Genetic Optimization Strategies" that explains how this plan is tailored to their unique genetic profile.
    """
    
    print(prompt)

    return prompt

def create_genetic_health_assessment_tools():
    """
    Create a structured tools schema for generating genetic health assessments.
    
    Returns:
        list: A list containing the function schema for genetic health assessment
    """
    tools = [
        {
            "function_declarations": [
                {
                    "name": "generate_structured_genetic_health_assessment",
                    "description": "Generate a structured health assessment for a diabetes patient that incorporates genetic profile insights.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "A concise summary paragraph of the patient's overall health status including genetic insights."
                            },
                            "diabetes_management_evaluation": {
                                "type": "string",
                                "description": "Overall evaluation of the patient's diabetes management status considering genetic factors."
                            },
                            "key_metrics_analysis": {
                                "type": "object",
                                "description": "Analysis of key health metrics compared to targets",
                                "properties": {
                                    "fasting_glucose": {"type": "string"},
                                    "postmeal_glucose": {"type": "string"},
                                    "hba1c": {"type": "string"}
                                }
                            },
                            "genetic_profile_overview": {
                                "type": "object",
                                "description": "Overview of key genetic factors affecting diabetes management",
                                "properties": {
                                    "carb_metabolism": {"type": "string"},
                                    "fat_metabolism": {"type": "string"},
                                    "inflammation_response": {"type": "string"},
                                    "caffeine_processing": {"type": "string"}
                                }
                            },
                            "potential_health_risks": {
                                "type": "string",
                                "description": "Description of potential health risks based on both standard assessment and genetic factors."
                            },
                            "suggested_diagnoses_and_care_plans": {
                                "type": "string",
                                "description": "Suggested diagnoses and care plans based on the assessment and genetic insights."
                            },
                            "areas_of_concern": {
                                "type": "string",
                                "description": "Areas of concern that should be discussed with a healthcare provider, including genetic considerations."
                            },
                            "personalized_recommendations": {
                                "type": "object",
                                "description": "Recommendations for health management tailored to genetic profile",
                                "properties": {
                                    "nutrition": {"type": "string"},
                                    "physical_activity": {"type": "string"},
                                    "medication_considerations": {"type": "string"},
                                    "lifestyle_modifications": {"type": "string"},
                                    "monitoring_approach": {"type": "string"}
                                }
                            }
                        },
                        "required": [
                            "summary", 
                            "diabetes_management_evaluation", 
                            "key_metrics_analysis", 
                            "genetic_profile_overview",
                            "potential_health_risks", 
                            "suggested_diagnoses_and_care_plans", 
                            "areas_of_concern", 
                            "personalized_recommendations"
                        ]
                    }
                }
            ]
        }
    ]
    
    return tools

def generate_genetic_health_assessment(user_data, genetic_profile):
    """
    Generate a health assessment using Gemini API based on both user health data and genetic profile.
    
    Args:
        user_data (dict): Dictionary containing user health data
        genetic_profile (dict): Dictionary containing user genetic profile
        
    Returns:
        str: Generated health assessment incorporating genetic insights
    """
    # Create a comprehensive prompt that includes both health and genetic data
    prompt = create_genetic_health_assessment_prompt(user_data, genetic_profile)
    
    # Initialize Gemini
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Get the genetic tools schema
    tools = create_genetic_health_assessment_tools()
    
    # Create model instance
    model = GenerativeModel(GEMINI_MODEL)
    
    # Generate response with function calling
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": """
                        You are an expert endocrinologist specializing in personalized diabetes care, metabolic health assessment and personalized medicine.
                        Your task is to transform patient health data and genetic information into actionable insights.
                        Analyze all available data to suggest personalized diagnoses and generate care plans that integrate genetic factors.
                        Focus on diabetes management, identify potential risks based on both medical metrics and genetic predispositions,
                        and recommend strategies tailored to the patient's unique genetic profile.
                        You must return your assessment in the exact structured format requested.
                        """
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        generation_config={"temperature": 0.2},
        tools=tools,
        tool_config={"function_calling_config": {"mode": "any"}}
    )
    
    # Check if function calling was used
    try:
        # Extract the structured response from function call
        if hasattr(response.candidates[0].content, 'parts') and hasattr(response.candidates[0].content.parts[0], 'function_call'):
            function_call = response.candidates[0].content.parts[0].function_call
            # Print for debugging
            print(f"Function call response: {function_call}")
            print(f"Args type: {type(function_call.args)}")
            print(f"Args: {function_call.args}")
            
            # Get the args safely - Gemini 1.5 API response handling
            try:
                if hasattr(function_call.args, 'to_dict'):
                    structured_assessment = function_call.args.to_dict()
                elif hasattr(function_call.args, '_asdict'):
                    structured_assessment = function_call.args._asdict()
                elif hasattr(function_call.args, '__dict__'):
                    structured_assessment = function_call.args.__dict__
                elif hasattr(function_call.args, '_pb'):
                    # Extract from _pb attribute which is a MessageMapContainer
                    pb_obj = function_call.args._pb
                    
                    # Try to extract data from _pb
                    try:
                        # Use items() method if available
                        extracted_data = {}
                        for key, value in pb_obj.items():
                            # Extract the actual value from the structure
                            str_value = str(value)
                            
                            # Parse number and string values
                            if 'number_value:' in str_value:
                                # Extract numeric value
                                num_str = str_value.split('number_value:')[1].strip()
                                try:
                                    # Try to convert to int first, then float
                                    extracted_data[key] = int(num_str)
                                except ValueError:
                                    try:
                                        extracted_data[key] = float(num_str)
                                    except ValueError:
                                        extracted_data[key] = num_str
                            elif 'string_value:' in str_value:
                                # Extract string value, removing quotes
                                str_content = str_value.split('string_value:')[1].strip()
                                extracted_data[key] = str_content.strip('"')
                            else:
                                # For other types, store string representation
                                extracted_data[key] = str_value
                        
                        # Create default metrics and components
                        key_metrics = {
                            "fasting_glucose": "Assessment of fasting glucose levels",
                            "postmeal_glucose": "Assessment of postmeal glucose levels",
                            "hba1c": "Assessment of HbA1c levels"
                        }
                        
                        genetic_profile = {
                            "carb_metabolism": "Your genetic carbohydrate metabolism profile",
                            "fat_metabolism": "Your genetic fat metabolism profile",
                            "inflammation_response": "Your genetic inflammation response profile",
                            "caffeine_processing": "Your genetic caffeine processing profile"
                        }
                        
                        recommendations = {
                            "nutrition": "Nutrition recommendations based on your genetic profile",
                            "physical_activity": "Physical activity recommendations based on your genetic profile",
                            "medication_considerations": "Medication considerations based on your genetic profile",
                            "lifestyle_modifications": "Lifestyle modification recommendations based on your genetic profile",
                            "monitoring_approach": "Monitoring approach recommendations based on your genetic profile"
                        }
                        
                        # Override with any extracted data
                        summary = extracted_data.get("summary", "Summary of your health assessment incorporating genetic factors")
                        diabetes_eval = extracted_data.get("diabetes_management_evaluation", "Your diabetes management assessment incorporating genetic insights")
                        health_risks = extracted_data.get("potential_health_risks", "Assessment of potential health risks based on your profile")
                        care_plans = extracted_data.get("suggested_diagnoses_and_care_plans", "Suggested care plans based on your health data and genetic profile")
                        areas_concern = extracted_data.get("areas_of_concern", "Areas to discuss with your healthcare provider")
                        
                        # Try to extract key metrics if available
                        if "key_metrics_analysis" in extracted_data:
                            key_metrics_str = str(extracted_data["key_metrics_analysis"])
                            
                            # Extract fasting glucose if available
                            if "fasting_glucose" in key_metrics_str:
                                fg_parts = key_metrics_str.split("fasting_glucose")
                                if len(fg_parts) > 1:
                                    fg_value = fg_parts[1].split(",")[0].strip(': "\'')
                                    key_metrics["fasting_glucose"] = fg_value
                            
                            # Extract postmeal glucose if available  
                            if "postmeal_glucose" in key_metrics_str:
                                pg_parts = key_metrics_str.split("postmeal_glucose")
                                if len(pg_parts) > 1:
                                    pg_value = pg_parts[1].split(",")[0].strip(': "\'')
                                    key_metrics["postmeal_glucose"] = pg_value
                            
                            # Extract hba1c if available
                            if "hba1c" in key_metrics_str:
                                hba_parts = key_metrics_str.split("hba1c")
                                if len(hba_parts) > 1:
                                    hba_value = hba_parts[1].split(",")[0].strip(': "\'')
                                    key_metrics["hba1c"] = hba_value
                        
                        # Try to extract genetic profile if available
                        if "genetic_profile_overview" in extracted_data:
                            genetic_str = str(extracted_data["genetic_profile_overview"])
                            
                            # Extract carb metabolism if available
                            if "carb_metabolism" in genetic_str:
                                carb_parts = genetic_str.split("carb_metabolism")
                                if len(carb_parts) > 1:
                                    carb_value = carb_parts[1].split(",")[0].strip(': "\'')
                                    genetic_profile["carb_metabolism"] = carb_value
                            
                            # Extract fat metabolism if available
                            if "fat_metabolism" in genetic_str:
                                fat_parts = genetic_str.split("fat_metabolism")
                                if len(fat_parts) > 1:
                                    fat_value = fat_parts[1].split(",")[0].strip(': "\'')
                                    genetic_profile["fat_metabolism"] = fat_value
                            
                            # Extract inflammation response if available
                            if "inflammation_response" in genetic_str:
                                infl_parts = genetic_str.split("inflammation_response")
                                if len(infl_parts) > 1:
                                    infl_value = infl_parts[1].split(",")[0].strip(': "\'')
                                    genetic_profile["inflammation_response"] = infl_value
                            
                            # Extract caffeine processing if available
                            if "caffeine_processing" in genetic_str:
                                caff_parts = genetic_str.split("caffeine_processing")
                                if len(caff_parts) > 1:
                                    caff_value = caff_parts[1].split(",")[0].strip(': "\'')
                                    genetic_profile["caffeine_processing"] = caff_value
                        
                        # Try to extract recommendations if available
                        if "personalized_recommendations" in extracted_data:
                            rec_str = str(extracted_data["personalized_recommendations"])
                            
                            if "nutrition" in rec_str:
                                try:
                                    nut_parts = rec_str.split("nutrition")
                                    if len(nut_parts) > 1:
                                        nut_value = nut_parts[1].split(",")[0].strip(': "\'')
                                        recommendations["nutrition"] = nut_value
                                except Exception:
                                    pass
                        
                        # Construct the full structured assessment
                        structured_assessment = {
                            "summary": summary,
                            "diabetes_management_evaluation": diabetes_eval,
                            "key_metrics_analysis": key_metrics,
                            "genetic_profile_overview": genetic_profile,
                            "potential_health_risks": health_risks,
                            "suggested_diagnoses_and_care_plans": care_plans,
                            "areas_of_concern": areas_concern,
                            "personalized_recommendations": recommendations
                        }
                        
                    except Exception as e:
                        print(f"Error iterating through _pb: {e}")
                        
                        # Fallback to string parsing if iteration fails
                        str_pb = str(pb_obj)
                        
                        # Extract summary if available
                        summary = "Summary of your health assessment incorporating genetic factors"
                        if "summary" in str_pb and "string_value" in str_pb:
                            try:
                                summary_parts = str_pb.split("'summary': string_value: ")
                                if len(summary_parts) > 1:
                                    summary = summary_parts[1].split("\n")[0].strip('"')
                            except Exception:
                                pass
                        
                        # Create default structured assessment
                        structured_assessment = {
                            "summary": summary,
                            "diabetes_management_evaluation": "Your diabetes management assessment incorporating genetic insights",
                            "key_metrics_analysis": {
                                "fasting_glucose": "Assessment of fasting glucose levels",
                                "postmeal_glucose": "Assessment of postmeal glucose levels",
                                "hba1c": "Assessment of HbA1c levels"
                            },
                            "genetic_profile_overview": {
                                "carb_metabolism": "Your genetic carbohydrate metabolism profile",
                                "fat_metabolism": "Your genetic fat metabolism profile",
                                "inflammation_response": "Your genetic inflammation response profile",
                                "caffeine_processing": "Your genetic caffeine processing profile"
                            },
                            "potential_health_risks": "Assessment of potential health risks based on your profile",
                            "suggested_diagnoses_and_care_plans": "Suggested care plans based on your health data and genetic profile",
                            "areas_of_concern": "Areas to discuss with your healthcare provider",
                            "personalized_recommendations": {
                                "nutrition": "Nutrition recommendations based on your genetic profile",
                                "physical_activity": "Physical activity recommendations based on your genetic profile",
                                "medication_considerations": "Medication considerations based on your genetic profile",
                                "lifestyle_modifications": "Lifestyle modification recommendations based on your genetic profile",
                                "monitoring_approach": "Monitoring approach recommendations based on your genetic profile"
                            }
                        }
                else:
                    # Try direct attribute access
                    # Extract basic assessment components
                    summary = getattr(function_call.args, "summary", "Summary of your health assessment incorporating genetic factors")
                    diabetes_eval = getattr(function_call.args, "diabetes_management_evaluation", "Your diabetes management assessment incorporating genetic insights")
                    
                    # Extract key metrics analysis with extra care
                    if hasattr(function_call.args, "key_metrics_analysis"):
                        key_metrics = function_call.args.key_metrics_analysis
                        # Ensure it has the expected structure or create default
                        if not isinstance(key_metrics, dict):
                            key_metrics = {
                                "fasting_glucose": "See assessment details",
                                "postmeal_glucose": "See assessment details",
                                "hba1c": "See assessment details"
                            }
                    else:
                        key_metrics = {
                            "fasting_glucose": "Assessment of fasting glucose levels",
                            "postmeal_glucose": "Assessment of postmeal glucose levels",
                            "hba1c": "Assessment of HbA1c levels"
                        }
                    
                    # Extract genetic profile overview
                    if hasattr(function_call.args, "genetic_profile_overview"):
                        genetic_profile = function_call.args.genetic_profile_overview
                        # Ensure it has the expected structure
                        if not isinstance(genetic_profile, dict):
                            genetic_profile = {
                                "carb_metabolism": "Your genetic carbohydrate metabolism profile",
                                "fat_metabolism": "Your genetic fat metabolism profile",
                                "inflammation_response": "Your genetic inflammation response profile",
                                "caffeine_processing": "Your genetic caffeine processing profile"
                            }
                    else:
                        genetic_profile = {
                            "carb_metabolism": "Your genetic carbohydrate metabolism profile",
                            "fat_metabolism": "Your genetic fat metabolism profile",
                            "inflammation_response": "Your genetic inflammation response profile",
                            "caffeine_processing": "Your genetic caffeine processing profile"
                        }
                    
                    # Extract remaining assessment components
                    health_risks = getattr(function_call.args, "potential_health_risks", "Assessment of potential health risks based on your profile")
                    care_plans = getattr(function_call.args, "suggested_diagnoses_and_care_plans", "Suggested care plans based on your health data and genetic profile")
                    areas_concern = getattr(function_call.args, "areas_of_concern", "Areas to discuss with your healthcare provider")
                    
                    # Extract personalized recommendations
                    if hasattr(function_call.args, "personalized_recommendations"):
                        recommendations = function_call.args.personalized_recommendations
                        # Ensure it has the expected structure
                        if not isinstance(recommendations, dict):
                            recommendations = {
                                "nutrition": "Nutrition recommendations based on your genetic profile",
                                "physical_activity": "Physical activity recommendations based on your genetic profile",
                                "medication_considerations": "Medication considerations based on your genetic profile",
                                "lifestyle_modifications": "Lifestyle modification recommendations based on your genetic profile",
                                "monitoring_approach": "Monitoring approach recommendations based on your genetic profile"
                            }
                    else:
                        recommendations = {
                            "nutrition": "Nutrition recommendations based on your genetic profile",
                            "physical_activity": "Physical activity recommendations based on your genetic profile",
                            "medication_considerations": "Medication considerations based on your genetic profile",
                            "lifestyle_modifications": "Lifestyle modification recommendations based on your genetic profile",
                            "monitoring_approach": "Monitoring approach recommendations based on your genetic profile"
                        }
                    
                    # Construct the full structured assessment
                    structured_assessment = {
                        "summary": summary,
                        "diabetes_management_evaluation": diabetes_eval,
                        "key_metrics_analysis": key_metrics,
                        "genetic_profile_overview": genetic_profile,
                        "potential_health_risks": health_risks,
                        "suggested_diagnoses_and_care_plans": care_plans,
                        "areas_of_concern": areas_concern,
                        "personalized_recommendations": recommendations
                    }
            except Exception as e:
                print(f"Error extracting args with attribute access: {e}")
                # Fallback to a basic structure if all methods fail
                structured_assessment = {
                    "summary": "Error parsing response from Gemini API",
                    "diabetes_management_evaluation": "Unable to generate assessment due to API response error",
                    "key_metrics_analysis": {
                        "fasting_glucose": "Data unavailable due to API error",
                        "postmeal_glucose": "Data unavailable due to API error",
                        "hba1c": "Data unavailable due to API error"
                    },
                    "genetic_profile_overview": {
                        "carb_metabolism": "Error processing response",
                        "fat_metabolism": "Error processing response",
                        "inflammation_response": "Error processing response",
                        "caffeine_processing": "Error processing response"
                    },
                    "potential_health_risks": "Assessment unavailable due to API error",
                    "suggested_diagnoses_and_care_plans": "Assessment unavailable due to API error",
                    "areas_of_concern": "Assessment unavailable due to API error",
                    "personalized_recommendations": {
                        "nutrition": "Unable to generate due to API error",
                        "physical_activity": "Unable to generate due to API error",
                        "medication_considerations": "Unable to generate due to API error",
                        "lifestyle_modifications": "Unable to generate due to API error",
                        "monitoring_approach": "Unable to generate due to API error"
                    }
                }
        else:
            # If no function call, process as regular text response
            print("No function call found in response. Full response:")
            print(response)
            # Try to extract any usable text
            try:
                text_response = response.text
                print(f"Text response: {text_response}")
                # Create a simple structured response
                structured_assessment = {
                    "summary": "The Gemini API did not return structured data in the expected format",
                    "diabetes_management_evaluation": "Model response format issue - see raw response below",
                    "key_metrics_analysis": {
                        "fasting_glucose": "See raw response",
                        "postmeal_glucose": "See raw response",
                        "hba1c": "See raw response"
                    },
                    "genetic_profile_overview": {
                        "carb_metabolism": "API returned non-structured response",
                        "fat_metabolism": "API returned non-structured response",
                        "inflammation_response": "API returned non-structured response",
                        "caffeine_processing": "API returned non-structured response"
                    },
                    "potential_health_risks": "See raw response below",
                    "suggested_diagnoses_and_care_plans": "See raw response below",
                    "areas_of_concern": "API response formatting issue",
                    "personalized_recommendations": {
                        "nutrition": "See raw response below",
                        "physical_activity": "See raw response below",
                        "medication_considerations": "See raw response below",
                        "lifestyle_modifications": "See raw response below",
                        "monitoring_approach": "See raw response below"
                    }
                }
            except Exception as e:
                print(f"Error processing text response: {e}")
                raise
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Response structure: {response}")
        # Create a minimal fallback structure
        structured_assessment = {
            "summary": f"Error: {str(e)}",
            "diabetes_management_evaluation": "Assessment unavailable due to technical error",
            "key_metrics_analysis": {
                "fasting_glucose": "Error processing response",
                "postmeal_glucose": "Error processing response",
                "hba1c": "Error processing response"
            },
            "genetic_profile_overview": {
                "carb_metabolism": "Error processing response",
                "fat_metabolism": "Error processing response",
                "inflammation_response": "Error processing response",
                "caffeine_processing": "Error processing response"
            },
            "potential_health_risks": "Error processing response",
            "suggested_diagnoses_and_care_plans": "Error processing response",
            "areas_of_concern": "Error processing response",
            "personalized_recommendations": {
                "nutrition": "Error processing response",
                "physical_activity": "Error processing response", 
                "medication_considerations": "Error processing response",
                "lifestyle_modifications": "Error processing response",
                "monitoring_approach": "Error processing response"
            }
        }
    
    # Store the structured data in the session state
    st.session_state.structured_genetic_health_assessment = structured_assessment
    
    health_assessment = structured_assessment
    
    return health_assessment

def create_genetic_health_assessment_prompt(user_data, genetic_profile):
    """
    Create a comprehensive prompt that includes both health and genetic data.
    
    Args:
        user_data (dict): Dictionary containing user health data
        genetic_profile (dict): Dictionary containing user genetic profile
        
    Returns:
        str: Combined prompt for generating a genetic health assessment
    """
    # Extract and format health data
    age = user_data.get('age', '')
    gender = user_data.get('gender', '')
    weight = user_data.get('weight', '')
    height = user_data.get('height', '')
    bmi = user_data.get('bmi', '')
    activity_level = user_data.get('activity_level', '')
    diabetes_type = user_data.get('diabetes_type', '')
    fasting_glucose = user_data.get('fasting_glucose', '')
    postmeal_glucose = user_data.get('postmeal_glucose', '')
    hba1c = user_data.get('hba1c', '')
    
    # Format medications and conditions
    medications = user_data.get('medications', '')
    medications_list = [med.strip() for med in medications.split('\n') if med.strip()]
    
    other_conditions = user_data.get('other_conditions', '')
    conditions_list = [condition.strip() for condition in other_conditions.split('\n') if condition.strip()]
    
    # Format genetic data
    carb_metabolism = genetic_profile.get('carb_metabolism', {})
    fat_metabolism = genetic_profile.get('fat_metabolism', {})
    vitamin_metabolism = genetic_profile.get('vitamin_metabolism', {})
    inflammation_response = genetic_profile.get('inflammation_response', {})
    caffeine_metabolism = genetic_profile.get('caffeine_metabolism', {})
    
    # Build the comprehensive prompt
    prompt = f"""
    Please provide a comprehensive health assessment for a patient with the following profile and genetic insights:
    
    ## Basic Information
    - Age: {age}
    - Gender: {gender}
    - Weight: {weight} kg
    - Height: {height} cm
    - BMI: {bmi}
    - Activity Level: {activity_level}
    
    ## Diabetes Information
    - Diabetes Type: {diabetes_type}
    - Fasting Blood Glucose: {fasting_glucose} mg/dL
    - Post-meal Blood Glucose: {postmeal_glucose} mg/dL
    - HbA1c: {hba1c}%
    
    ## Medications
    {chr(10).join(f"- {med}" for med in medications_list) if medications_list else "- None specified"}
    
    ## Other Health Conditions
    {chr(10).join(f"- {condition}" for condition in conditions_list) if conditions_list else "- None specified"}
    
    ## Genetic Profile
    
    ### Carbohydrate Metabolism
    - Sensitivity: {carb_metabolism.get('carb_sensitivity', 'Normal')}
    - Explanation: {carb_metabolism.get('explanation', 'No specific genetic variations detected')}
    - Genetic Recommendations:
      {chr(10).join(f"  - {rec}" for rec in carb_metabolism.get('recommendations', [])) if carb_metabolism.get('recommendations') else "  - No specific recommendations"}
    
    ### Fat Metabolism
    - Sensitivity to Saturated Fat: {fat_metabolism.get('saturated_fat_sensitivity', 'Normal')}
    - Explanation: {fat_metabolism.get('explanation', 'No specific genetic variations detected')}
    - Genetic Recommendations:
      {chr(10).join(f"  - {rec}" for rec in fat_metabolism.get('recommendations', [])) if fat_metabolism.get('recommendations') else "  - No specific recommendations"}
    
    ### Inflammation Response
    - Inflammatory Response: {inflammation_response.get('inflammatory_response', 'Normal')}
    - Explanation: {inflammation_response.get('explanation', 'No specific genetic variations detected')}
    - Genetic Recommendations:
      {chr(10).join(f"  - {rec}" for rec in inflammation_response.get('recommendations', [])) if inflammation_response.get('recommendations') else "  - No specific recommendations"}
    
    ### Caffeine Metabolism
    - Caffeine Processing: {caffeine_metabolism.get('caffeine_metabolism', 'Normal')}
    - Explanation: {caffeine_metabolism.get('explanation', 'No specific genetic variations detected')}
    - Genetic Recommendations:
      {chr(10).join(f"  - {rec}" for rec in caffeine_metabolism.get('recommendations', [])) if caffeine_metabolism.get('recommendations') else "  - No specific recommendations"}
    
    ## Overall Genetic Summary
    {genetic_profile.get('overall_summary', 'No significant genetic variations affecting diabetes management were detected.')}
    
    ## Key Genetic Recommendations
    {chr(10).join(f"- {rec}" for rec in genetic_profile.get('key_recommendations', [])) if genetic_profile.get('key_recommendations') else "- No specific genetic-based recommendations"}
    
    ## Requested Assessment
    Based on both the patient's health data and genetic profile, please provide:
    
    1. An overall health assessment that incorporates genetic insights
    2. Analysis of key health metrics with genetic context
    3. Specific genetic factors affecting diabetes management
    4. Potential health risks based on both standard and genetic factors
    5. Personalized diagnosis and care plans integrating genetic insights
    6. Areas of concern for healthcare provider discussion
    7. Detailed personalized recommendations for:
       - Nutrition (based on genetic metabolism factors)
       - Physical activity (considering genetic factors)
       - Medication considerations (with genetic context)
       - Lifestyle modifications (personalized to genetic profile)
       - Monitoring approach (optimized for genetic factors)
    
    Include more detailed information for each subsection

    Format the assessment in the structured format requested by the tools interface.
    """
    
    return prompt