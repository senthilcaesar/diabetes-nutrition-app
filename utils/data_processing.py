# Data Collection and Preprocessing Prompt

## User Data Prompt
def get_health_metrics_prompt(user_data):
    """
    Create a prompt to analyze and process user health metrics.
    
    Parameters:
    user_data (dict): Dictionary containing user health data
    
    Returns:
    str: Formatted prompt for the LLM
    """
    prompt = f"""
    Analyze the following health metrics for a person with diabetes and identify key nutritional considerations:
    
    ## Health Data
    - Age: {user_data.get('age')}
    - Gender: {user_data.get('gender')}
    - Weight (kg): {user_data.get('weight')}
    - Height (cm): {user_data.get('height')}
    - Activity Level: {user_data.get('activity_level')}
    - Diabetes Type: {user_data.get('diabetes_type')}
    - Blood Glucose Levels:
        - Fasting: {user_data.get('fasting_glucose')} mg/dL
        - Post-meal average: {user_data.get('postmeal_glucose')} mg/dL
    - HbA1c: {user_data.get('hba1c')}%
    - Blood Pressure: {user_data.get('blood_pressure')}
    - Cholesterol:
        - Total: {user_data.get('total_cholesterol')} mg/dL
        - LDL: {user_data.get('ldl')} mg/dL
        - HDL: {user_data.get('hdl')} mg/dL
        - Triglycerides: {user_data.get('triglycerides')} mg/dL
    - Existing Dietary Restrictions: {user_data.get('dietary_restrictions')}
    - Current Medications: {user_data.get('medications')}
    - Other Health Conditions: {user_data.get('other_conditions')}
    
    ## Current Diet Information
    - Typical Daily Meals: {user_data.get('typical_meals')}
    - Snacking Habits: {user_data.get('snacking_habits')}
    - Food Preferences: {user_data.get('food_preferences')}
    - Cultural Food Considerations: {user_data.get('cultural_foods')}
    - Average Daily Caloric Intake: {user_data.get('daily_calories')} calories
    - Carbohydrate Intake: {user_data.get('carb_intake')} g
    - Protein Intake: {user_data.get('protein_intake')} g
    - Fat Intake: {user_data.get('fat_intake')} g
    - Sugar Intake: {user_data.get('sugar_intake')} g
    - Fiber Intake: {user_data.get('fiber_intake')} g
    
    Based on this data, provide a comprehensive analysis of the individual's current metabolic health and identify the key nutritional factors that should be addressed in a personalized nutrition plan.
    """
    return prompt


def get_socioeconomic_prompt(user_data):
    """
    Create a prompt to analyze and process user socioeconomic factors.
    
    Parameters:
    user_data (dict): Dictionary containing user socioeconomic data
    
    Returns:
    str: Formatted prompt for the LLM
    """
    prompt = f"""
    Analyze the following socioeconomic factors for creating an accessible and effective nutrition plan:
    
    ## Socioeconomic Factors
    - Location: {user_data.get('location')}
    - Geographic Setting (Urban/Rural): {user_data.get('geographic_setting')}
    - Income Level: {user_data.get('income_level')}
    - Education Level: {user_data.get('education_level')}
    - Literacy Level: {user_data.get('literacy_level')}
    - Language Preferences: {user_data.get('language_preferences')}
    - Access to Technology: {user_data.get('technology_access')}
    - Access to Healthcare: {user_data.get('healthcare_access')}
    - Local Food Availability: {user_data.get('local_food_availability')}
    - Grocery Budget: {user_data.get('grocery_budget')} per week
    - Cooking Facilities: {user_data.get('cooking_facilities')}
    - Time Available for Meal Preparation: {user_data.get('meal_prep_time')}
    - Family Size: {user_data.get('family_size')}
    - Support System: {user_data.get('support_system')}
    
    Based on these socioeconomic factors, recommend adaptations to make the nutrition plan accessible, practical, and effective for this individual, considering their specific circumstances and constraints.
    """
    return prompt


def combine_data_for_analysis(health_data, socioeconomic_data):
    """
    Combine health and socioeconomic data for comprehensive analysis.
    
    Parameters:
    health_data (dict): Dictionary containing user health data
    socioeconomic_data (dict): Dictionary containing user socioeconomic data
    
    Returns:
    str: Combined prompt for the LLM
    """
    health_prompt = get_health_metrics_prompt(health_data)
    socio_prompt = get_socioeconomic_prompt(socioeconomic_data)
    
    combined_prompt = f"""
    # Comprehensive Analysis for Personalized Diabetes Nutrition Plan
    
    {health_prompt}
    
    {socio_prompt}
    
    Based on both the health metrics and socioeconomic factors provided above, create a holistic analysis that addresses the following:
    
    1. Key nutritional needs based on the individual's diabetes status and overall health
    2. Practical constraints and opportunities based on socioeconomic factors
    3. Recommendations for adapting the nutrition plan to the individual's specific circumstances
    4. Suggestions for presentation format based on literacy level and technology access
    5. Potential barriers to adherence and strategies to overcome them
    
    Provide this analysis in a structured format that can be used to generate a personalized nutrition plan.
    """
    
    return combined_prompt


## Data Preprocessing Functions

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_health_data(health_data):
    """
    Preprocess and validate health data.
    
    Parameters:
    health_data (dict): Dictionary containing user health data
    
    Returns:
    dict: Preprocessed health data
    """
    processed_data = health_data.copy()
    
    # Convert values to appropriate types
    if 'age' in processed_data and processed_data['age']:
        processed_data['age'] = int(processed_data['age'])
    
    if 'weight' in processed_data and processed_data['weight']:
        processed_data['weight'] = float(processed_data['weight'])
    
    if 'height' in processed_data and processed_data['height']:
        processed_data['height'] = float(processed_data['height'])
        
        # Calculate BMI if height and weight are available
        if 'weight' in processed_data and processed_data['weight']:
            height_m = processed_data['height'] / 100  # Convert cm to m
            processed_data['bmi'] = round(processed_data['weight'] / (height_m ** 2), 1)
    
    # Convert glucose values to float
    for key in ['fasting_glucose', 'postmeal_glucose', 'hba1c']:
        if key in processed_data and processed_data[key]:
            processed_data[key] = float(processed_data[key])
    
    # Calculate estimated daily calorie needs using Harris-Benedict equation
    if all(key in processed_data and processed_data[key] for key in ['age', 'weight', 'height', 'gender', 'activity_level']):
        # Base Metabolic Rate (BMR)
        if processed_data['gender'].lower() == 'male':
            bmr = 88.362 + (13.397 * processed_data['weight']) + (4.799 * processed_data['height']) - (5.677 * processed_data['age'])
        else:
            bmr = 447.593 + (9.247 * processed_data['weight']) + (3.098 * processed_data['height']) - (4.330 * processed_data['age'])
        
        # Activity multiplier
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly active': 1.375,
            'moderately active': 1.55,
            'very active': 1.725,
            'extra active': 1.9
        }
        
        activity = processed_data['activity_level'].lower()
        multiplier = activity_multipliers.get(activity, 1.2)  # Default to sedentary if not found
        
        processed_data['estimated_calorie_needs'] = round(bmr * multiplier)
    
    return processed_data


def preprocess_socioeconomic_data(socio_data):
    """
    Preprocess and validate socioeconomic data.
    
    Parameters:
    socio_data (dict): Dictionary containing user socioeconomic data
    
    Returns:
    dict: Preprocessed socioeconomic data with additional derived features
    """
    processed_data = socio_data.copy()
    
    # Calculate food accessibility score (0-10)
    food_access_factors = {
        'geographic_setting': {'urban': 8, 'suburban': 7, 'rural': 5},
        'income_level': {'low': 4, 'medium': 7, 'high': 9},
        'local_food_availability': {'limited': 3, 'moderate': 6, 'abundant': 9}
    }
    
    access_score = 0
    count = 0
    
    for factor, ratings in food_access_factors.items():
        if factor in processed_data and processed_data[factor]:
            value = processed_data[factor].lower()
            if value in ratings:
                access_score += ratings[value]
                count += 1
    
    if count > 0:
        processed_data['food_accessibility_score'] = round(access_score / count, 1)
    
    # Determine plan complexity level based on education and literacy
    if 'education_level' in processed_data and 'literacy_level' in processed_data:
        edu = processed_data['education_level'].lower() if processed_data['education_level'] else ''
        lit = processed_data['literacy_level'].lower() if processed_data['literacy_level'] else ''
        
        if ('elementary' in edu or 'primary' in edu or 'low' in lit or 'basic' in lit):
            processed_data['plan_complexity'] = 'simple'
        elif ('high school' in edu or 'secondary' in edu or 'moderate' in lit or 'average' in lit):
            processed_data['plan_complexity'] = 'moderate'
        elif ('college' in edu or 'university' in edu or 'bachelor' in edu or 'master' in edu or 'doctorate' in edu or 'high' in lit):
            processed_data['plan_complexity'] = 'advanced'
        else:
            processed_data['plan_complexity'] = 'moderate'  # Default to moderate
    
    # Format guidance based on literacy and technology access
    if 'literacy_level' in processed_data and 'technology_access' in processed_data:
        lit = processed_data['literacy_level'].lower() if processed_data['literacy_level'] else ''
        tech = processed_data['technology_access'].lower() if processed_data['technology_access'] else ''
        
        if 'low' in lit or 'basic' in lit:
            processed_data['format_guidance'] = 'highly visual with minimal text'
        elif 'limited' in tech:
            processed_data['format_guidance'] = 'printable with visual aids'
        else:
            processed_data['format_guidance'] = 'balanced text and visuals'
    
    return processed_data
