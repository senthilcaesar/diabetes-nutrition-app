"""
Genetic LLM integration module for the Diabetes Nutrition Plan application.
Contains functions for integrating genetic data into the nutrition plan.
"""

import json
import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel
from typing import Dict, List, Optional, Any
from utils.genetic_data_helpers import (
    create_default_genetic_nutritional_overview,
    create_default_genetic_nutrition_plan,
    process_extracted_genetic_nutrition_data
)

GEMINI_MODEL = "gemini-1.5-flash"

def format_structured_genetic_nutrition_plan(structured_data):
    """
    Convert the structured genetic nutrition plan data into four separate sections:
    1. Overview - General nutrition plan overview with light genetic context
    2. Meal Plan - Genetically optimized meal plan
    3. Genetic Optimization - Dedicated genetic insights section
    4. Recipes & Tips - Recipe suggestions and blood sugar management tips
    
    Handles various input formats including MapComposite objects from Gemini API.
    
    Args:
        structured_data: The structured nutrition plan data, which can be a dict, 
                        MapComposite object, or other format that needs processing
    
    Returns:
        tuple: (overview, meal_plan, genetic_section, recipes_tips) sections as formatted text
    """
    try:
        # SECTION 1: OVERVIEW
        overview = ""
        
        # First, handle potential MapComposite object or other non-dict formats
        processed_data = {}
        
        # If structured_data is None or empty, create default data
        if not structured_data:
            print("Warning: Empty structured data received")
            processed_data = create_default_genetic_nutrition_plan()
        else:
            # Check if it's a dict already
            if isinstance(structured_data, dict):
                processed_data = structured_data
            else:
                # Try different methods to extract data from non-dict objects
                try:
                    # Try converting to dict if possible
                    if hasattr(structured_data, 'to_dict'):
                        processed_data = structured_data.to_dict()
                    elif hasattr(structured_data, '_asdict'):
                        processed_data = structured_data._asdict()
                    elif hasattr(structured_data, '__dict__'):
                        processed_data = structured_data.__dict__
                    elif hasattr(structured_data, '_pb'):
                        # Extract from _pb attribute (MapComposite objects from Gemini API)
                        pb_obj = structured_data._pb
                        
                        # Try to extract data using items() method
                        extracted_data = {}
                        for key, value in pb_obj.items():
                            # Extract the actual value based on the structure
                            str_value = str(value)
                            
                            # Process different value types
                            if 'number_value:' in str_value:
                                # Extract numeric values
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
                                # Extract string values, removing quotes
                                str_content = str_value.split('string_value:')[1].strip()
                                extracted_data[key] = str_content.strip('"')
                            elif 'list_value' in str_value:
                                # Extract list values
                                items = []
                                parts = str_value.split('string_value:')
                                for i in range(1, len(parts)):
                                    item_value = parts[i].split('"')[1] if '"' in parts[i] else parts[i].strip()
                                    items.append(item_value)
                                extracted_data[key] = items
                            elif 'struct_value' in str_value:
                                # For complex nested structures, store as string for now
                                # Will need deeper parsing for specific fields later
                                extracted_data[key] = str_value
                            else:
                                # For other types, store string representation
                                extracted_data[key] = str_value
                        
                        # Process the extracted data into standard nutrition plan format
                        processed_data = process_extracted_genetic_nutrition_data(extracted_data)
                    else:
                        # Try to access some expected attributes directly as fallback
                        processed_data = create_default_genetic_nutrition_plan()
                        # Try to populate with any available data
                        if hasattr(structured_data, "introduction"):
                            processed_data["introduction"] = getattr(structured_data, "introduction", "Welcome to your personalized genetic nutrition plan")
                        if hasattr(structured_data, "nutritional_overview"):
                            processed_data["nutritional_overview"] = getattr(structured_data, "nutritional_overview")
                except Exception as e:
                    print(f"Error processing structured data: {e}")
                    # Fall back to default structure
                    processed_data = create_default_genetic_nutrition_plan()
        
        # Now format the processed data
                
        # Get nutritional overview with safe fallbacks - ensure it's a dict
        if "nutritional_overview" not in processed_data or not isinstance(processed_data["nutritional_overview"], dict):
            processed_data["nutritional_overview"] = create_default_genetic_nutritional_overview()
            
        nutritional_overview = processed_data["nutritional_overview"]
            
        # Daily Caloric Target with safe fallbacks
        if "daily_caloric_target" not in nutritional_overview or not isinstance(nutritional_overview["daily_caloric_target"], dict):
            nutritional_overview["daily_caloric_target"] = {"calories": 2000, "explanation": "This caloric target is based on your metabolic needs."}
            
        caloric = nutritional_overview["daily_caloric_target"]
        calories = caloric.get("calories", 2000)
        explanation = caloric.get("explanation", "This caloric target is based on your metabolic needs.")
            
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
    Create a simplified tools schema for generating genetically optimized nutrition plans.
    
    Returns:
        list: A list containing the function schema for genetic nutrition plan
    """
    tools = [
        {
            "function_declarations": [
                {
                    "name": "generate_structured_genetic_nutrition_plan",
                    "description": "Generate a structured nutrition plan for a diabetes patient that incorporates genetic insights alongside health data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "introduction": {
                                "type": "string",
                                "description": "A personalized introduction to the nutrition plan"
                            },
                            "nutritional_overview": {
                                "type": "object",
                                "description": "Overview of the nutritional approach with genetic optimization",
                                "properties": {
                                    "daily_calories": {"type": "number"},
                                    "carbs_percentage": {"type": "number"},
                                    "protein_percentage": {"type": "number"},
                                    "fat_percentage": {"type": "number"},
                                    "meal_timing": {"type": "string"}
                                }
                            },
                            "genetic_optimization_strategies": {
                                "type": "object",
                                "description": "Nutrition strategies based on genetic profile",
                                "properties": {
                                    "carb_metabolism": {"type": "string"},
                                    "fat_metabolism": {"type": "string"},
                                    "inflammation_response": {"type": "string"}
                                }
                            },
                            "recommended_foods": {
                                "type": "object",
                                "description": "Foods recommended based on genetic profile",
                                "properties": {
                                    "carbohydrates": {"type": "array", "items": {"type": "string"}},
                                    "proteins": {"type": "array", "items": {"type": "string"}},
                                    "fats": {"type": "array", "items": {"type": "string"}}
                                }
                            },
                            "foods_to_limit": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "food_category": {"type": "string"},
                                        "reason": {"type": "string"}
                                    }
                                }
                            },
                            "day1_meals": {
                                "type": "object",
                                "properties": {
                                    "breakfast": {"type": "string"},
                                    "lunch": {"type": "string"},
                                    "dinner": {"type": "string"}
                                }
                            },
                            "day2_meals": {
                                "type": "object",
                                "properties": {
                                    "breakfast": {"type": "string"},
                                    "lunch": {"type": "string"},
                                    "dinner": {"type": "string"}
                                }
                            },
                            "day3_meals": {
                                "type": "object",
                                "properties": {
                                    "breakfast": {"type": "string"},
                                    "lunch": {"type": "string"},
                                    "dinner": {"type": "string"}
                                }
                            },
                            "blood_sugar_management": {
                                "type": "object",
                                "properties": {
                                    "hypoglycemia_prevention": {"type": "string"},
                                    "hyperglycemia_management": {"type": "string"}
                                }
                            }
                        },
                        "required": ["introduction", "nutritional_overview", "genetic_optimization_strategies", "recommended_foods", "foods_to_limit"]
                    }
                }
            ]
        }
    ]
    
    return tools

def generate_genetic_enhanced_nutrition_plan(user_data, genetic_profile):
    """
    Generate a nutrition plan that incorporates genetic insights.
    Uses robust handling for Gemini API MapComposite objects.
    
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
            
            # Extract the args using our helper functions that handle different response types
            try:
                # Try converting to dict if possible
                if hasattr(function_call.args, 'to_dict'):
                    structured_plan = function_call.args.to_dict()
                elif hasattr(function_call.args, '_asdict'):
                    structured_plan = function_call.args._asdict()
                elif hasattr(function_call.args, '__dict__'):
                    structured_plan = function_call.args.__dict__
                elif hasattr(function_call.args, '_pb'):
                    # Extract from _pb attribute (MapComposite objects from Gemini API)
                    pb_obj = function_call.args._pb
                    
                    # Extract data from MapComposite object
                    extracted_data = {}
                    for key, value in pb_obj.items():
                        # Extract the actual value based on the structure
                        str_value = str(value)
                        
                        # Process different value types
                        if 'number_value:' in str_value:
                            # Extract numeric values
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
                            # Extract string values, removing quotes
                            str_content = str_value.split('string_value:')[1].strip()
                            extracted_data[key] = str_content.strip('"')
                        elif 'list_value' in str_value:
                            # Extract list values
                            items = []
                            parts = str_value.split('string_value:')
                            for i in range(1, len(parts)):
                                item_value = parts[i].split('"')[1] if '"' in parts[i] else parts[i].strip()
                                items.append(item_value)
                            extracted_data[key] = items
                        elif 'struct_value' in str_value:
                            # For complex nested structures, store as string for now
                            extracted_data[key] = str_value
                        else:
                            # For other types, store string representation
                            extracted_data[key] = str_value
                    
                    # Process the extracted data into standard nutrition plan format
                    structured_plan = process_extracted_genetic_nutrition_data(extracted_data)
                else:
                    # Try to access some expected attributes directly as fallback
                    structured_plan = create_default_genetic_nutrition_plan()
                    # Try to populate with any available data
                    if hasattr(function_call.args, "introduction"):
                        structured_plan["introduction"] = getattr(function_call.args, "introduction", "Welcome to your personalized genetic nutrition plan")
                    if hasattr(function_call.args, "nutritional_overview"):
                        structured_plan["nutritional_overview"] = getattr(function_call.args, "nutritional_overview")
            except Exception as e:
                print(f"Error extracting args with attribute access: {e}")
                # Fallback to default structure if all methods fail
                structured_plan = create_default_genetic_nutrition_plan()
        else:
            # If no function call, process as regular text response
            print("No function call found in response. Full response:")
            print(response)
            # Try to extract any usable text
            try:
                text_response = response.text
                print(f"Text response: {text_response}")
                # Create a default structured plan with a note about the non-structured response
                structured_plan = create_default_genetic_nutrition_plan()
                structured_plan["introduction"] = "Model did not use function calling. Here's a default plan with insights from your genetic profile."
            except Exception as e:
                print(f"Error processing text response: {e}")
                structured_plan = create_default_genetic_nutrition_plan()
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Response structure: {response}")
        # Create a minimal fallback structure
        structured_plan = create_default_genetic_nutrition_plan()
        structured_plan["introduction"] = f"Error processing API response: {str(e)}. Here's a default plan based on your genetic profile."
    
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
    Create a simplified tools schema for generating genetic health assessments.
    
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
                                "description": "A concise summary of the patient's health status including genetic insights"
                            },
                            "diabetes_management_evaluation": {
                                "type": "string",
                                "description": "Evaluation of diabetes management with genetic context"
                            },
                            "glucose_analysis": {
                                "type": "string",
                                "description": "Analysis of glucose levels and HbA1c"
                            },
                            "genetic_insights": {
                                "type": "string",
                                "description": "Key genetic factors affecting diabetes management"
                            },
                            "health_risks": {
                                "type": "string",
                                "description": "Potential health risks based on data and genetics"
                            },
                            "care_plans": {
                                "type": "string",
                                "description": "Suggested care plans integrating genetic insights"
                            },
                            "nutrition_recommendations": {
                                "type": "string",
                                "description": "Nutrition guidance based on genetic profile"
                            },
                            "lifestyle_recommendations": {
                                "type": "string",
                                "description": "Activity and lifestyle guidance based on genetic factors"
                            }
                        },
                        "required": [
                            "summary", 
                            "diabetes_management_evaluation",
                            "glucose_analysis",
                            "genetic_insights", 
                            "health_risks", 
                            "care_plans", 
                            "nutrition_recommendations",
                            "lifestyle_recommendations"
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
    Uses robust handling for Gemini API MapComposite objects.
    
    Args:
        user_data (dict): Dictionary containing user health data
        genetic_profile (dict): Dictionary containing user genetic profile
        
    Returns:
        dict: Generated health assessment incorporating genetic insights as a structured dictionary
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
    
    # Default structure for genetic health assessment - simplified version
    default_assessment = {
        "summary": "Summary of your health assessment incorporating genetic factors",
        "diabetes_management_evaluation": "Your diabetes management assessment incorporating genetic insights",
        "glucose_analysis": "Analysis of your glucose levels and HbA1c with genetic context",
        "genetic_insights": "Overview of how your genetic profile affects diabetes management",
        "health_risks": "Assessment of potential health risks based on your profile and genetics",
        "care_plans": "Suggested care plans based on your health data and genetic profile",
        "nutrition_recommendations": "Nutrition guidance tailored to your genetic profile",
        "lifestyle_recommendations": "Activity and lifestyle recommendations based on your genetic factors",
        # Include backward compatibility fields
        "potential_health_risks": "Assessment of potential health risks based on your profile",
        "suggested_diagnoses_and_care_plans": "Suggested care plans based on your health data and genetic profile",
        "recommendations": "Personalized recommendations for health improvement"
    }
    
    # Check if function calling was used
    try:
        # Extract the structured response from function call
        if hasattr(response.candidates[0].content, 'parts') and hasattr(response.candidates[0].content.parts[0], 'function_call'):
            function_call = response.candidates[0].content.parts[0].function_call
            # Print for debugging
            print(f"Function call response: {function_call}")
            print(f"Args type: {type(function_call.args)}")
            
            # Extract the args using various methods
            try:
                # Try converting to dict if possible
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
                            
                            # Process different value types
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
                            elif 'list_value' in str_value:
                                # Extract list values
                                items = []
                                parts = str_value.split('string_value:')
                                for i in range(1, len(parts)):
                                    item_value = parts[i].split('"')[1] if '"' in parts[i] else parts[i].strip()
                                    items.append(item_value)
                                extracted_data[key] = items
                            elif 'struct_value' in str_value:
                                # For complex nested structures, store as string for now
                                extracted_data[key] = str_value
                            else:
                                # For other types, store string representation
                                extracted_data[key] = str_value
                        
                        # Process the extracted data into simplified assessment format
                        structured_assessment = default_assessment.copy()
                        
                        # Simple fields - directly map from extracted data to structured assessment
                        field_mappings = {
                            "summary": "summary",
                            "diabetes_management_evaluation": "diabetes_management_evaluation",
                            "glucose_analysis": "glucose_analysis",
                            "genetic_insights": "genetic_insights",
                            "health_risks": "health_risks",
                            "care_plans": "care_plans",
                            "nutrition_recommendations": "nutrition_recommendations",
                            "lifestyle_recommendations": "lifestyle_recommendations"
                        }
                        
                        # Try to fill in each field from extracted data
                        for target_field, source_field in field_mappings.items():
                            if source_field in extracted_data:
                                structured_assessment[target_field] = extracted_data[source_field]
                        
                        # Map old field names to new ones for backward compatibility
                        if "potential_health_risks" in extracted_data and "health_risks" not in extracted_data:
                            structured_assessment["health_risks"] = extracted_data["potential_health_risks"]
                            
                        if "suggested_diagnoses_and_care_plans" in extracted_data and "care_plans" not in extracted_data:
                            structured_assessment["care_plans"] = extracted_data["suggested_diagnoses_and_care_plans"]
                        
                        # Try to extract key metrics and convert to simplified glucose_analysis field
                        if "key_metrics_analysis" in extracted_data and "glucose_analysis" not in extracted_data:
                            key_metrics_str = str(extracted_data["key_metrics_analysis"])
                            
                            # Create a simplified text version of glucose analysis
                            glucose_text = "Analysis of your glucose metrics: "
                            metrics_added = False
                            
                            for metric in ["fasting_glucose", "postmeal_glucose", "hba1c"]:
                                if metric in key_metrics_str:
                                    parts = key_metrics_str.split(metric)
                                    if len(parts) > 1:
                                        value_parts = parts[1].split("string_value:")
                                        if len(value_parts) > 1:
                                            value = value_parts[1].split('"')[1] if '"' in value_parts[1] else value_parts[1].strip()
                                            glucose_text += f"{metric.replace('_', ' ')}: {value}. "
                                            metrics_added = True
                            
                            if metrics_added:
                                structured_assessment["glucose_analysis"] = glucose_text
                        
                        # Try to extract genetic profile and convert to simplified genetic_insights field
                        if "genetic_profile_overview" in extracted_data and "genetic_insights" not in extracted_data:
                            genetic_str = str(extracted_data["genetic_profile_overview"])
                            
                            # Create a simplified text version of genetic insights
                            genetic_text = "Your genetic insights include: "
                            insights_added = False
                            
                            genetic_factors = ["carb_metabolism", "fat_metabolism", "inflammation_response", "caffeine_processing"]
                            for factor in genetic_factors:
                                if factor in genetic_str:
                                    factor_parts = genetic_str.split(factor)
                                    if len(factor_parts) > 1:
                                        factor_value_parts = factor_parts[1].split("string_value:")
                                        if len(factor_value_parts) > 1:
                                            factor_value = factor_value_parts[1].split('"')[1] if '"' in factor_value_parts[1] else factor_value_parts[1].strip()
                                            genetic_text += f"{factor.replace('_', ' ')}: {factor_value}. "
                                            insights_added = True
                            
                            if insights_added:
                                structured_assessment["genetic_insights"] = genetic_text
                        
                        # Try to extract recommendations and convert to simplified nutrition and lifestyle fields
                        if "personalized_recommendations" in extracted_data:
                            rec_str = str(extracted_data["personalized_recommendations"])
                            
                            # Try to extract nutrition recommendations
                            if "nutrition" in rec_str and "nutrition_recommendations" not in extracted_data:
                                parts = rec_str.split("nutrition")
                                if len(parts) > 1:
                                    value_parts = parts[1].split("string_value:")
                                    if len(value_parts) > 1:
                                        value = value_parts[1].split('"')[1] if '"' in value_parts[1] else value_parts[1].strip()
                                        structured_assessment["nutrition_recommendations"] = value
                            
                            # Try to create combined lifestyle recommendations if not already present
                            if "lifestyle_recommendations" not in extracted_data:
                                lifestyle_text = "Lifestyle recommendations based on your genetic profile: "
                                recs_added = False
                                
                                lifestyle_fields = ["physical_activity", "lifestyle_modifications", "monitoring_approach"]
                                for field in lifestyle_fields:
                                    if field in rec_str:
                                        parts = rec_str.split(field)
                                        if len(parts) > 1:
                                            value_parts = parts[1].split("string_value:")
                                            if len(value_parts) > 1:
                                                value = value_parts[1].split('"')[1] if '"' in value_parts[1] else value_parts[1].strip()
                                                lifestyle_text += f"{field.replace('_', ' ')}: {value}. "
                                                recs_added = True
                                
                                if recs_added:
                                    structured_assessment["lifestyle_recommendations"] = lifestyle_text
                    except Exception as e:
                        print(f"Error processing MapComposite: {e}")
                        structured_assessment = default_assessment.copy()
                else:
                    # Try direct attribute access as fallback with simplified schema
                    structured_assessment = default_assessment.copy()
                    
                    # Map of fields to check with fallbacks
                    field_mappings = {
                        "summary": ["summary"],
                        "diabetes_management_evaluation": ["diabetes_management_evaluation"],
                        "glucose_analysis": ["glucose_analysis", "key_metrics_analysis"],
                        "genetic_insights": ["genetic_insights", "genetic_profile_overview"],
                        "health_risks": ["health_risks", "potential_health_risks"],
                        "care_plans": ["care_plans", "suggested_diagnoses_and_care_plans"],
                        "nutrition_recommendations": ["nutrition_recommendations"],
                        "lifestyle_recommendations": ["lifestyle_recommendations"]
                    }
                    
                    # Try each field with potential fallbacks
                    for target_field, source_fields in field_mappings.items():
                        for source_field in source_fields:
                            if hasattr(function_call.args, source_field):
                                structured_assessment[target_field] = getattr(function_call.args, source_field)
                                break
            except Exception as e:
                print(f"Error extracting args with attribute access: {e}")
                # Fallback to the default structure if all methods fail
                structured_assessment = default_assessment.copy()
                structured_assessment["summary"] = f"Error parsing Gemini API response: {str(e)}. Here's a default assessment based on your health data and genetic profile."
        else:
            # If no function call, use default structure with a note
            print("No function call found in response. Full response:")
            print(response)
            structured_assessment = default_assessment.copy()
            structured_assessment["summary"] = "The Gemini API response did not contain structured data in the expected format. Here's a default assessment based on your health data and genetic profile."
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Response structure: {response}")
        # Create a minimal fallback structure
        structured_assessment = default_assessment.copy()
        structured_assessment["summary"] = f"Error processing API response: {str(e)}. Here's a default assessment based on your health data and genetic profile."
    
    # Store the structured data in the session state
    st.session_state.structured_genetic_health_assessment = structured_assessment
    
    return structured_assessment

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