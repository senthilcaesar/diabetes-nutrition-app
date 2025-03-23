"""
Genetic LLM integration module for the Diabetes Nutrition Plan application.
Contains functions for integrating genetic data into the nutrition plan.
"""

from openai import OpenAI
from typing import Dict, List, Optional, Any

def generate_genetic_enhanced_nutrition_plan(user_data: Dict, genetic_profile: Dict, api_key: str) -> str:
    """
    Generate a nutrition plan that incorporates genetic insights.
    
    Args:
        user_data (Dict): Dictionary containing user health and socioeconomic data
        genetic_profile (Dict): Dictionary containing genetic nutrition profile
        api_key (str): OpenAI API key
        
    Returns:
        str: Generated nutrition plan with genetic insights
    """
    prompt = create_genetic_nutrition_plan_prompt(user_data, genetic_profile)
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.5-preview",  # Adjust based on availability and needs
        messages=[
            {"role": "system", "content": "You are a medical nutrition specialist with expertise in both diabetes management and nutrigenomics. Create a personalized nutrition plan that integrates both health data and genetic insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2500
    )
    
    nutrition_plan = response.choices[0].message.content.strip()
    return nutrition_plan

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

def generate_genetic_health_assessment(user_data: Dict, genetic_profile: Dict, api_key: str) -> str:
    """
    Generate a health assessment that incorporates genetic insights.
    
    Args:
        user_data (Dict): Dictionary containing user health data
        genetic_profile (Dict): Dictionary containing genetic nutrition profile
        api_key (str): OpenAI API key
        
    Returns:
        str: Generated health assessment with genetic insights
    """
    prompt = create_genetic_health_assessment_prompt(user_data, genetic_profile)
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.5-preview",  # Use GPT-4 for more comprehensive medical analysis
        messages=[
            {"role": "system", "content": """
            You are an expert endocrinologist specializing in personalized diabetes care, metabolic health assessment, and nutrigenomics.
            Your task is to transform patient data and genetic information into actionable insights by analyzing all available patient data,
            suggesting diagnoses and generating care plans that integrate genetic factors.
            Please focus on diabetes management, identify potential risks and areas of concern, and recommend strategies for improvement
            based on both standard medical protocols and genetic insights.
            """
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Lower temperature for more consistent medical information
        max_tokens=1500
    )
    
    health_assessment = response.choices[0].message.content.strip()
    return health_assessment

def create_genetic_health_assessment_prompt(user_data: Dict, genetic_profile: Dict) -> str:
    """
    Create a prompt for generating a health assessment with genetic insights.
    
    Args:
        user_data (Dict): Dictionary containing user health data
        genetic_profile (Dict): Dictionary containing genetic nutrition profile
        
    Returns:
        str: Generated prompt
    """
    # Extract and format key health metrics (same as in llm_integration.py)
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
    
    # Format genetic insights
    genetic_info = """
    ## Genetic Insights
    """
    
    # Add overall genetic summary
    genetic_info += f"""
    ### Overall Genetic Summary
    {genetic_profile.get('overall_summary', '')}
    
    Key Genetic-Based Recommendations:
    """
    for rec in genetic_profile.get('key_recommendations', []):
        genetic_info += f"- {rec}\n"
    
    # Add carbohydrate metabolism insights
    carb_metabolism = genetic_profile.get("carb_metabolism", {})
    genetic_info += f"""
    ### Carbohydrate Metabolism
    - Carbohydrate Sensitivity: {carb_metabolism.get('carb_sensitivity', 'normal')}
    - Explanation: {carb_metabolism.get('explanation', '')}
    """
    
    # Add fat metabolism insights
    fat_metabolism = genetic_profile.get("fat_metabolism", {})
    genetic_info += f"""
    ### Fat Metabolism
    - Saturated Fat Sensitivity: {fat_metabolism.get('saturated_fat_sensitivity', 'normal')}
    - Explanation: {fat_metabolism.get('explanation', '')}
    """
    
    # Add inflammation response insights
    inflammation_response = genetic_profile.get("inflammation_response", {})
    genetic_info += f"""
    ### Inflammation Response
    - Inflammatory Response: {inflammation_response.get('inflammatory_response', 'normal')}
    - Explanation: {inflammation_response.get('explanation', '')}
    """
    
    # Build the complete prompt
    prompt = f"""
    Please provide a comprehensive health assessment for a patient with the following profile, integrating both their standard health metrics AND their genetic insights:
    
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
    
    {genetic_info}
    
    ## Requested Assessment
    Please provide:
    1. An overall evaluation of the patient's diabetes management, integrating genetic insights
    2. Analysis of their key metrics and how they compare to recommended targets
    3. Identification of potential health risks based on both their standard health profile AND genetic factors
    4. Specific areas where genetic factors may be impacting their metabolic health
    5. Personalized recommendations that incorporate both standard diabetes care AND genetic optimization
    6. Specific areas of concern that should be discussed with a healthcare provider
    
    Format the assessment in clear sections with headings, and begin with a summary of the most important points. Include a specific section titled "Genetic Factors and Metabolism" that explains how their genetic profile impacts their diabetes management.
    """
    print(prompt)
    
    return prompt