"""
Genetic LLM integration module for the Diabetes Nutrition Plan application.
Contains functions for integrating genetic data into the nutrition plan.
"""

from openai import OpenAI
import json
import streamlit as st
from typing import Dict, List, Optional, Any

GPT_MODEL = "gpt-4.1-2025-04-14"

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
    # SECTION 1: OVERVIEW
    overview = ""
    
    # Daily Caloric Target
    caloric = structured_data["nutritional_overview"]["daily_caloric_target"]
    overview += f"### 🔥 Daily Caloric Target: {caloric['calories']} calories\n\n"
    overview += f"{caloric['explanation']}\n\n"
    
    # Macronutrient Distribution with visualization-like formatting
    overview += "### 🥗 Macronutrient Distribution\n\n"
    
    macro = structured_data["nutritional_overview"]["macronutrient_distribution"]
    
    # Create a visually appealing macronutrient table
    overview += "| Nutrient | Percentage | Grams |\n"
    overview += "|----------|------------|-------|\n"
    overview += f"| **Carbohydrates** | {macro['carbohydrates']['percentage']}% | {macro['carbohydrates']['grams']}g |\n"
    overview += f"| **Protein** | {macro['protein']['percentage']}% | {macro['protein']['grams']}g |\n"
    overview += f"| **Fat** | {macro['fat']['percentage']}% | {macro['fat']['grams']}g |\n\n"
    
    # Carbohydrate recommendations - keep genetic mentions minimal here
    overview += f"**Carbohydrates:** {macro['carbohydrates']['recommendations']}\n\n"
    overview += f"**Protein:** {macro['protein']['recommendations']}\n\n"
    overview += f"**Fat:** {macro['fat']['recommendations']}\n\n"
    
    # Meal Structure with clock icon
    structure = structured_data["nutritional_overview"]["meal_structure"]
    overview += "### ⏰ Meal Structure and Timing\n\n"
    overview += f"**Meal Frequency:** {structure['meal_frequency']}\n\n"
    overview += f"**Timing Recommendations:** {structure['timing_recommendations']}\n\n"
    overview += f"**Portion Guidance:** {structure['portion_guidance']}\n\n"
    
    overview += "---\n\n"
    
    # Recommended Foods section with thumbs up icon
    overview += "### Recommended Foods\n\n"

    foods = structured_data["recommended_foods"]

    # Create a table for foods with headers
    overview += "| Category | Recommended Foods |\n"
    overview += "|----------|-------------------|\n"

    # Add carbohydrates to table
    carbs_list = ", ".join(foods["carbohydrates"])
    overview += f"| 🌾 **Carbohydrates** | {carbs_list} |\n"

    # Add proteins to table
    proteins_list = ", ".join(foods["proteins"])
    overview += f"| 🥩 **Proteins** | {proteins_list} |\n"

    # Add fats to table
    fats_list = ", ".join(foods["fats"])
    overview += f"| 🥑 **Fats** | {fats_list} |\n"

    # Add vegetables to table
    vegetables_list = ", ".join(foods["vegetables"])
    overview += f"| 🥦 **Vegetables** | {vegetables_list} |\n"

    # Add fruits to table
    fruits_list = ", ".join(foods["fruits"])
    overview += f"| 🍎 **Fruits** | {fruits_list} |\n"

    # Add beverages to table
    beverages_list = ", ".join(foods["beverages"])
    overview += f"| 🥤 **Beverages** | {beverages_list} |\n\n"
    
    # SECTION 2: MEAL PLAN
    meal_plan = ""
    
    # Sample Meal Plans with calendar icon and badge indicating genetic optimization
    # meal_plan += """## 📅 Meal Plan


    meal_plans = structured_data["meal_plans"]

    # Create tables for each day
    for day_num in range(1, 4):
        day_key = f'day{day_num}'
        day_meals = meal_plans[day_key]
        
        meal_plan += f"### 🍽️ Day {day_num}\n\n"
        
        # Create table header
        meal_plan += "| Meal | Description |\n"
        meal_plan += "|------|-------------|\n"
        
        # Add breakfast
        meal_plan += f"| 🌞 **Breakfast** | {day_meals['breakfast']} |\n"
        
        # Add morning snack if available
        if day_meals.get('morning_snack'):
            meal_plan += f"| 🥪 **Morning Snack** | {day_meals['morning_snack']} |\n"
        
        # Add lunch
        meal_plan += f"| 🍲 **Lunch** | {day_meals['lunch']} |\n"
        
        # Add afternoon snack if available
        if day_meals.get('afternoon_snack'):
            meal_plan += f"| 🍏 **Afternoon Snack** | {day_meals['afternoon_snack']} |\n"
        
        # Add dinner
        meal_plan += f"| 🍽️ **Dinner** | {day_meals['dinner']} |\n"
        
        # Add evening snack if available
        if day_meals.get('evening_snack'):
            meal_plan += f"| 🥛 **Evening Snack** | {day_meals['evening_snack']} |\n"
        
        meal_plan += "\n\n"
    
    # SECTION 3: GENETIC OPTIMIZATION TAB - This section is fully dedicated to genetic insights
    genetic_section = ""
    
    
    # Add Genetic Optimization Strategies section
    if "genetic_optimization_strategies" in structured_data:
        genetic = structured_data["genetic_optimization_strategies"]
        
        # Add each genetic strategy with appropriate formatting
        if "carb_metabolism" in genetic:
            genetic_section += f"""
### Carbohydrate Metabolism

<div style="
    background-color: #E8F5E9; 
    border-left: 5px solid #4CAF50;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{genetic['carb_metabolism']}
</div>
"""
        
        if "fat_metabolism" in genetic:
            genetic_section += f"""
### Fat Metabolism

<div style="
    background-color: #FFF8E1; 
    border-left: 5px solid #FFC107;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{genetic['fat_metabolism']}
</div>
"""
        
        if "inflammation_response" in genetic:
            genetic_section += f"""
### Inflammation Response

<div style="
    background-color: #FFEBEE; 
    border-left: 5px solid #F44336;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{genetic['inflammation_response']}
</div>
"""
            
        if "nutrient_processing" in genetic:
            genetic_section += f"""
### Nutrient Processing

<div style="
    background-color: #E1F5FE; 
    border-left: 5px solid #03A9F4;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{genetic['nutrient_processing']}
</div>
"""
            
        if "caffeine_metabolism" in genetic:
            genetic_section += f"""
### Caffeine Metabolism

<div style="
    background-color: #F3E5F5; 
    border-left: 5px solid #9C27B0;
    padding: 15px; 
    border-radius: 5px;
    margin-bottom: 20px;
">
{genetic['caffeine_metabolism']}
</div>
"""
    
    # Add specific foods section based on genetics
    genetic_section += """
### Recommended Foods Based on Your Genetic Profile
"""
    
    # Create a list of genetically recommended foods from the structured data
    # This would typically be custom-filtered from the recommended_foods based on genetic profile
    genetic_section += "| Category | Reason | Foods |\n"
    genetic_section += "|----------|--------|-------|\n"
    
    # Add some genetic-specific food recommendations
    # These would normally come from the structured data, but we're creating examples
    if "genetic_food_recommendations" in structured_data:
        for rec in structured_data.get("genetic_food_recommendations", []):
            genetic_section += f"| **{rec.get('category', '')}** | {rec.get('reason', '')} | {rec.get('foods', '')} |\n"
    else:
        # Default recommendations if not provided
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
    
    # SECTION 4: RECIPES & TIPS
    recipes_tips = ""
    
    # Simple Recipes with chef hat icon
    if "recipes" in structured_data and structured_data["recipes"]:
        
        for recipe in structured_data["recipes"]:
            recipes_tips += "<div class='recipe-card'>\n\n"
            recipes_tips += f"## {recipe['name']}\n\n"
            recipes_tips += f"**⏱️ Preparation Time:** {recipe['prep_time']}\n\n"
            recipes_tips += f"**🛒 Ingredients:**\n{recipe['ingredients']}\n\n"
            recipes_tips += f"**📝 Instructions:**\n{recipe['instructions']}\n\n"
            recipes_tips += f"**💪 Nutritional Benefits:** {recipe['nutritional_benefits']}\n\n"
            
            # Add genetic note if available
            if 'genetic_note' in recipe:
                recipes_tips += f"**🧬 Genetic Benefit:** {recipe['genetic_note']}\n\n"
                
            recipes_tips += "</div>\n\n"
        
        recipes_tips += "---\n\n"

    # Foods to Limit section with stop sign icon
    recipes_tips += "# 🛑 Foods to Limit or Avoid\n\n"

    # Create table header
    recipes_tips += "| Food Category | Why to Limit | Better Alternatives |\n"
    recipes_tips += "|---------------|-------------|---------------------|\n"

    # Add each food item as a row in the table
    for item in structured_data["foods_to_limit"]:
        recipes_tips += f"| **{item['food_category']}** | {item['reason']} | {item['alternatives']} |\n"

    recipes_tips += "---\n\n"
    
    # Blood Sugar Management with chart icon
    if "blood_sugar_management" in structured_data:
        recipes_tips += "# 📈 Blood Sugar Management Strategies\n\n"
        
        bsm = structured_data["blood_sugar_management"]
        
        recipes_tips += "<div class='management-card'>\n\n"
        recipes_tips += "### 📉 Preventing Low Blood Sugar (Hypoglycemia)\n\n"
        recipes_tips += f"{bsm['hypoglycemia_prevention']}\n\n"
        recipes_tips += "</div>\n\n"
        
        recipes_tips += "<div class='management-card'>\n\n"
        recipes_tips += "### 📈 Managing High Blood Sugar (Hyperglycemia)\n\n"
        recipes_tips += f"{bsm['hyperglycemia_management']}\n\n"
        recipes_tips += "</div>\n\n"
        
        recipes_tips += "<div class='management-card'>\n\n"
        recipes_tips += "### ⏰ Meal Timing Strategies\n\n"
        recipes_tips += f"{bsm['meal_timing_strategies']}\n\n"
        recipes_tips += "</div>\n\n"
        
        recipes_tips += "<div class='management-card'>\n\n"
        recipes_tips += "### 🥕 Smart Snacking\n\n"
        recipes_tips += f"{bsm['snack_recommendations']}\n\n"
        recipes_tips += "</div>\n\n"
    
    # Make sure to return all four values
    return overview, meal_plan, genetic_section, recipes_tips

def create_genetic_nutrition_plan_tools():
    """
    Create a structured tools schema for generating genetically optimized nutrition plans.
    
    Returns:
        list: A list containing the function schema for genetic nutrition plan
    """
    tools = [
        {
            "type": "function",
            "function": {
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
        }
    ]
    
    return tools

def generate_genetic_enhanced_nutrition_plan(user_data, genetic_profile, api_key):
    """
    Generate a nutrition plan that incorporates genetic insights.
    
    Args:
        user_data (dict): Dictionary containing user health and socioeconomic data
        genetic_profile (dict): Dictionary containing genetic nutrition profile
        api_key (str): OpenAI API key
        
    Returns:
        tuple: (nutrition_plan, overview, meal_plan, genetic_section, recipes_tips) - complete plan and individual sections
    """
    prompt = create_genetic_nutrition_plan_prompt(user_data, genetic_profile)
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a medical nutrition specialist with expertise in both diabetes management and nutrigenomics. Create a personalized nutrition plan that integrates both health data and genetic insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        tools=create_genetic_nutrition_plan_tools(),
        tool_choice={"type": "function", "function": {"name": "generate_structured_genetic_nutrition_plan"}}
    )
    
    # Extract the structured response
    function_call = response.choices[0].message.tool_calls[0]
    structured_plan = json.loads(function_call.function.arguments)
    
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
            "type": "function",
            "function": {
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
        }
    ]
    
    return tools

def generate_genetic_health_assessment(user_data, genetic_profile, api_key):
    """
    Generate a health assessment using OpenAI API based on both user health data and genetic profile.
    
    Args:
        user_data (dict): Dictionary containing user health data
        genetic_profile (dict): Dictionary containing user genetic profile
        api_key (str): OpenAI API key
        
    Returns:
        str: Generated health assessment incorporating genetic insights
    """
    # Create a comprehensive prompt that includes both health and genetic data
    prompt = create_genetic_health_assessment_prompt(user_data, genetic_profile)
    
    client = OpenAI(api_key=api_key)
    
    # Get the genetic tools schema
    tools = create_genetic_health_assessment_tools()
    
    response = client.chat.completions.create(
        model=GPT_MODEL,  # Use appropriate model
        messages=[
            {"role": "system", "content": """
            You are an expert endocrinologist specializing in personalized diabetes care, metabolic health assessment and personalized medicine.
            Your task is to transform patient health data and genetic information into actionable insights.
            Analyze all available data to suggest personalized diagnoses and generate care plans that integrate genetic factors.
            Focus on diabetes management, identify potential risks based on both medical metrics and genetic predispositions,
            and recommend strategies tailored to the patient's unique genetic profile.
            You must return your assessment in the exact structured format requested.
            """
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Lower temperature for more consistent medical information
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "generate_structured_genetic_health_assessment"}}
    )
    
    # Extract the structured response
    function_call = response.choices[0].message.tool_calls[0]
    structured_assessment = json.loads(function_call.function.arguments)
    
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