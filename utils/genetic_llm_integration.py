"""
Genetic LLM integration module for the Diabetes Nutrition Plan application.
Contains functions for integrating genetic data into the nutrition plan.
"""

from openai import OpenAI
import json
import streamlit as st
from typing import Dict, List, Optional, Any
from utils.llm_integration import create_nutrition_plan_tools, format_structured_nutrition_plan

GPT_MODEL = "gpt-4o"

def generate_genetic_enhanced_nutrition_plan(user_data, genetic_profile, api_key):
    """
    Generate a nutrition plan that incorporates genetic insights.
    
    Returns:
        tuple: (nutrition_plan, overview, meal_plan, recipes_tips) - complete plan and individual sections
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
        tools=create_nutrition_plan_tools(),
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