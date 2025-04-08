from openai import OpenAI
import json
import streamlit as st

GPT_MODEL = "gpt-4.5-preview-2025-02-27"  # Specify the model to use

# This module handles all OpenAI API interactions for the diabetes nutrition plan application
def initialize_openai_client(api_key):
    """Initialize and return an OpenAI client with the provided API key."""
    return OpenAI(api_key=api_key)

def create_health_assessment_tools():
    """
    Create a structured tools schema for generating health assessments with the specified format.
    
    Returns:
        list: A list containing the function schema for health assessment
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_structured_health_assessment",
                "description": "Generate a structured health assessment for a diabetes patient based on their health data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A concise summary paragraph of the patient's overall health status and key concerns."
                        },
                        "diabetes_management_evaluation": {
                            "type": "string",
                            "description": "Overall evaluation of the patient's diabetes management status."
                        },
                        "key_metrics_analysis": {
                            "type": "object",
                            "description": "Analysis of key health metrics compared to targets.",
                            "properties": {
                                "fasting_glucose": {"type": "string"},
                                "postmeal_glucose": {"type": "string"},
                                "hba1c": {"type": "string"}
                            }
                        },
                        "potential_health_risks": {
                            "type": "string",
                            "description": "Description of potential health risks based on the assessment."
                        },
                        "suggested_diagnoses_and_care_plans": {
                            "type": "string",
                            "description": "Suggested diagnoses and care plans based on the assessment."
                        },
                        "areas_of_concern": {
                            "type": "string",
                            "description": "Areas of concern that should be discussed with a healthcare provider."
                        },
                        "recommendations": {
                            "type": "array",
                            "description": "List of specific recommendations for health management improvement.",
                            "items": {
                                "type": "string"
                            }
                        },
                        "genetic_factors": {
                            "type": "object",
                            "description": "Genetic insights related to diabetes management (if genetic data is available)",
                            "properties": {
                                "summary": {"type": "string"},
                                "impact_on_management": {"type": "string"},
                                "specific_recommendations": {"type": "string"}
                            }
                        }
                    },
                    "required": ["summary", "diabetes_management_evaluation", "key_metrics_analysis", "potential_health_risks", "suggested_diagnoses_and_care_plans", "areas_of_concern", "recommendations"]
                }
            }
        }
    ]
    
    return tools

def generate_health_assessment(user_data, api_key):
    """Generate a health assessment using OpenAI API based on user health data."""
    prompt = create_health_assessment_prompt(user_data)
    
    client = OpenAI(api_key=api_key)
    
    # Get the tools schema
    tools = create_health_assessment_tools()
    
    response = client.chat.completions.create(
        model=GPT_MODEL,  # Use GPT-4 for more comprehensive medical analysis
        messages=[
            {"role": "system", "content": """
            You are an expert endocrinologist specializing in personalized diabetes care and metabolic 
            health assessment and provides endocrine consultations. You lead active clinical research programs in the fields of osteoporosis and obesity/metabolic diseases.
            Your task is to transform patient data into actionable insights by analyzing all available patient data, suggesting diagnoses and generating care plans.
            Please focus on diabetes management, identify potential risks and areas of concern, and recommend 
            strategies for improvement. You must return your assessment in the exact structured format requested.
            """
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature for more consistent medical information
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "generate_structured_health_assessment"}}
    )
    
    # Extract the structured response
    function_call = response.choices[0].message.tool_calls[0]
    structured_assessment = json.loads(function_call.function.arguments)
    
    # Store the structured data in the session state for display
    st.session_state.structured_health_assessment = structured_assessment
        
    # For backward compatibility, still return the formatted assessment string
    health_assessment = structured_assessment
    return health_assessment

def create_health_assessment_prompt(user_data):
    """Create a prompt for generating a health assessment."""
    
    # Extract and format key health metrics
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
    
    # Format medications and other conditions for better prompt structure
    medications = user_data.get('medications', '')
    medications_list = [med.strip() for med in medications.split('\n') if med.strip()]
    
    other_conditions = user_data.get('other_conditions', '')
    conditions_list = [condition.strip() for condition in other_conditions.split('\n') if condition.strip()]
    
    # Get dietary restrictions
    dietary_restrictions = user_data.get('dietary_restrictions', 'None')
    
    # Build the prompt
    prompt = f"""
    Please provide a comprehensive health assessment for a patient with the following profile:
    
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
    
    ## Dietary Restrictions
    - {dietary_restrictions}
    
    ## Requested Assessment
    Please provide:
    1. An overall evaluation of the patient's diabetes management
    2. Analysis of their key metrics and how they compare to recommended targets
    3. Identification of potential health risks based on their profile
    4. Suggestion of diagnoses and care plans
    5. Specific areas of concern that should be discussed with a healthcare provider
    6. Recommendations for improving their health management
    
    Format the assessment in clear sections with headings, and begin with a summary of the most important points and include more detailed information.
    """
    
    print(prompt)

    return prompt

def create_nutrition_plan_tools():
    """
    Create a structured tools schema for generating nutrition plans.
    
    Returns:
        list: A list containing the function schema for nutrition plan
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_structured_nutrition_plan",
                "description": "Generate a structured nutrition plan for a diabetes patient based on their health and socioeconomic data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "introduction": {
                            "type": "string",
                            "description": "A personalized introduction to the nutrition plan that addresses the individual's specific situation."
                        },
                        "nutritional_overview": {
                            "type": "object",
                            "description": "Overview of the nutritional approach and guidelines",
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
                        "recommended_foods": {
                            "type": "object",
                            "description": "Foods that are recommended for diabetes management",
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
                            "description": "Foods that should be limited or avoided",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "food_category": {"type": "string"},
                                    "reason": {"type": "string"},
                                    "alternatives": {"type": "string"}
                                }
                            }
                        },
                        "meal_plans": {
                            "type": "object",
                            "description": "Sample meal plans for different days",
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
                            "description": "Simple recipes tailored to the individual's preferences and resources",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "ingredients": {"type": "string"},
                                    "instructions": {"type": "string"},
                                    "prep_time": {"type": "string"},
                                    "nutritional_benefits": {"type": "string"}
                                }
                            }
                        },
                        "blood_sugar_management": {
                            "type": "object",
                            "description": "Strategies for managing blood sugar through nutrition",
                            "properties": {
                                "hypoglycemia_prevention": {"type": "string"},
                                "hyperglycemia_management": {"type": "string"},
                                "meal_timing_strategies": {"type": "string"},
                                "snack_recommendations": {"type": "string"}
                            }
                        },

                    },
                    "required": ["introduction", "nutritional_overview", "recommended_foods", "foods_to_limit", "meal_plans"]
                }
            }
        }
    ]
    
    return tools


    """Generate a personalized nutrition plan using OpenAI."""
    prompt = create_nutrition_plan_prompt(user_data)
    
    print(prompt)

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",  # Adjust based on availability and needs
        messages=[
            {"role": "system", "content": "You are a medical nutrition specialist with expertise in diabetes management. Create a personalized nutrition plan based on the provided health and socioeconomic data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    nutrition_plan = response.choices[0].message.content.strip()
    print(nutrition_plan)
    return nutrition_plan

def generate_nutrition_plan(user_data, api_key):
    """
    Generate a personalized nutrition plan using OpenAI.
    
    Returns:
        tuple: (nutrition_plan, overview, meal_plan, recipes_tips) - complete plan and individual sections
    """
    prompt = create_nutrition_plan_prompt(user_data)
    
    client = OpenAI(api_key=api_key)
    
    # Get the tools schema
    tools = create_nutrition_plan_tools()
    
    response = client.chat.completions.create(
        model=GPT_MODEL,  # Adjust based on availability and needs
        messages=[
            {"role": "system", "content": "You are a medical nutrition specialist with expertise in diabetes management. Create a personalized nutrition plan based on the provided health and socioeconomic data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "generate_structured_nutrition_plan"}}
    )
    
    # Extract the structured response
    function_call = response.choices[0].message.tool_calls[0]
    structured_plan = json.loads(function_call.function.arguments)
    
    # Format the structured data into separate sections
    overview, meal_plan, recipes_tips = format_structured_nutrition_plan(structured_plan)
    
    # Also create a complete plan by combining all sections (for backward compatibility)
    nutrition_plan = overview + "\n" + meal_plan + "\n" + recipes_tips
    
    return nutrition_plan, overview, meal_plan, recipes_tips

def format_structured_nutrition_plan(structured_data):
    """
    Convert the structured nutrition plan data into three separate sections:
    1. Overview
    2. Meal Plan
    3. Recipes & Tips
    
    Returns:
        tuple: (overview, meal_plan, recipes_tips) sections as formatted text
    """
    # SECTION 1: OVERVIEW
    overview = ""
        
    # Nutritional Overview section with chart icon
    overview += ""
    
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
    
    # Carbohydrate recommendations in styled box
    overview += f"**Carbohydrates:** {macro['carbohydrates']['recommendations']}\n\n"
    
    # Protein recommendations in styled box
    overview += f"**Protein:** {macro['protein']['recommendations']}\n\n"
    
    # Fat recommendations in styled box
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
    
    overview += "</div>\n\n"
        
    # SECTION 2: MEAL PLAN
    meal_plan = ""
    
    # Sample Meal Plans with calendar icon
    meal_plan += ""

    meal_plans = structured_data["meal_plans"]

    # Create tables for each day
    for day_num in range(1, 4):
        day_key = f'day{day_num}'
        day_meals = meal_plans[day_key]
        
        meal_plan += f"## 🍽️ Day {day_num}\n\n"
        
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
    
    
    # SECTION 3: RECIPES & TIPS
    recipes_tips = ""
    
        # Simple Recipes with chef hat icon
    if "recipes" in structured_data and structured_data["recipes"]:
        
        for recipe in structured_data["recipes"]:
            recipes_tips += "<div class='recipe-card'>\n\n"
            recipes_tips += f"### {recipe['name']}\n\n"
            recipes_tips += f"**⏱️ Preparation Time:** {recipe['prep_time']}\n\n"
            recipes_tips += f"**🛒 Ingredients:**\n{recipe['ingredients']}\n\n"
            recipes_tips += f"**📝 Instructions:**\n{recipe['instructions']}\n\n"
            recipes_tips += f"**💪 Nutritional Benefits:** {recipe['nutritional_benefits']}\n\n"
            recipes_tips += "</div>\n\n"
        
        recipes_tips += "---\n\n"

    # Foods to Limit section with stop sign icon
    recipes_tips += "## Foods to Limit or Avoid\n\n"

    # Create table header
    recipes_tips += "| Food Category | Why to Limit | Better Alternatives |\n"
    recipes_tips += "|---------------|-------------|---------------------|\n"

    # Add each food item as a row in the table
    for item in structured_data["foods_to_limit"]:
        recipes_tips += f"| **{item['food_category']}** | {item['reason']} | {item['alternatives']} |\n"

    recipes_tips += "---\n\n"
        
    
    # Blood Sugar Management with chart icon
    if "blood_sugar_management" in structured_data:
        recipes_tips += "## Blood Sugar Management Strategies\n\n"
        
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
    
    return overview, meal_plan, recipes_tips
    
def create_nutrition_plan_prompt(user_data):
    """Create a prompt for generating a nutrition plan."""
    diabetes_type = user_data.get('diabetes_type', 'Type 2')
    cultural_foods = user_data.get('cultural_foods', 'No specific cultural preferences')
    literacy_level = user_data.get('literacy_level', 'moderate')
    income_level = user_data.get('income_level', 'medium')
    grocery_budget = user_data.get('grocery_budget', 'moderate')
    local_foods = user_data.get('local_food_availability', 'moderate')
    
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
    
    socio_info = f"""
    ## Socioeconomic Considerations
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
    
    prompt = f"""
    Create a comprehensive, personalized nutrition plan for an individual with {diabetes_type} diabetes based on the following data:
    
    {health_info}
    
    {socio_info}
    
    ## Plan Specifications
    Please create a nutrition plan that includes:
    
    1. Daily caloric target and macronutrient distribution (carbs, protein, fat)
    2. Recommended meal structure (timing and composition)
    3. A sample 3-day meal plan with specific locally available foods
    4. Simple recipe ideas that require minimal preparation time and basic cooking facilities
    5. Guidance on proper portion sizes using common household items as references
    6. Specific foods to avoid or limit
    7. Foods that can help stabilize blood sugar
    
    The plan should be:
    - Culturally appropriate and incorporate local food options
    - Affordable within the specified budget
    - Easy to understand with the specified literacy level in mind
    - Practical considering the individual's living conditions and cooking facilities
    - Specifically designed to help manage diabetes while addressing other health conditions

    Include more detailed nutritional information, rationale for recommendations.
    
    Return the plan in a well-formatted structure with clear sections.
    """
    
    print(prompt)
    return prompt

def generate_visual_guidance(nutrition_plan, literacy_level, plan_complexity, api_key):
    """Generate visual guidance descriptions based on the nutrition plan."""
    prompt = f"""
    Create detailed descriptions for visual aids to accompany the following nutrition plan:
    
    NUTRITION PLAN:
    {nutrition_plan}
    
    The user has a {literacy_level} literacy level and the plan complexity is {plan_complexity}.
    
    For each key concept in the nutrition plan, describe a simple, clear visual that could help communicate the information. These visual descriptions should:
    
    1. Focus on concrete representations of abstract concepts
    2. Use familiar objects, symbols, and scenarios
    3. Employ color coding for categorization (e.g., green for "good" foods, red for "avoid" foods)
    4. Include visual portion guides using common household objects
    5. Illustrate meal timing and structure
    6. Show cause-and-effect relationships related to food and blood sugar
    
    {'Include detailed visual descriptions that represent key information with minimal reliance on text.' if 'low' in literacy_level else 'Balance visual elements with text to reinforce key concepts.'}
    
    Provide 5-7 detailed visual descriptions covering the most important aspects of the nutrition plan.
    
    For each visual, provide:
    1. A clear title
    2. A detailed description of what the visual should look like
    3. The key message this visual is meant to convey
    """
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a visual health educator specialized in creating accessible diabetes education materials."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    
    visual_guidance = response.choices[0].message.content.strip()
    return visual_guidance