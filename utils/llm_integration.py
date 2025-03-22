from openai import OpenAI

# This module handles all OpenAI API interactions for the diabetes nutrition plan application

def initialize_openai_client(api_key):
    """Initialize and return an OpenAI client with the provided API key."""
    return OpenAI(api_key=api_key)

def generate_health_assessment(user_data, api_key):
    """Generate a health assessment using OpenAI API based on user health data."""
    prompt = create_health_assessment_prompt(user_data)
    
    print(prompt)

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.5-preview",  # Use GPT-4 for more comprehensive medical analysis
        messages=[
            {"role": "system", "content": """
            You are an expert endocrinologist specializing in personalized diabetes care and metabolic health assessment.
            Your tasks is to transform patient data into actionable insights by analyzing all available patient data, suggesting diagnoses and generating care plans.
            Please focus on diabetes management, identify potential risks and areas of concern, and recommend strategies for improvement.
            """
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Lower temperature for more consistent medical information
        max_tokens=1500
    )
    
    health_assessment = response.choices[0].message.content.strip()
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
    
    Format the assessment in clear sections with headings, and begin with a summary of the most important points.
    """
    
    return prompt

def generate_nutrition_plan(user_data, api_key):
    """Generate a personalized nutrition plan using OpenAI."""
    prompt = create_nutrition_plan_prompt(user_data)
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.5-preview",  # Adjust based on availability and needs
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

def create_nutrition_plan_prompt(user_data):
    """Create a prompt for generating a nutrition plan."""
    diabetes_type = user_data.get('diabetes_type', 'Type 2')
    format_guidance = user_data.get('format_guidance', 'balanced text and visuals')
    plan_complexity = user_data.get('plan_complexity', 'moderate')
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
    
    {'' if plan_complexity != 'simple' else 'Make the plan extremely simple, using basic language, visual cues, and minimal text. Focus on practical, actionable guidance rather than detailed explanations.'}
    
    {'' if plan_complexity != 'advanced' else 'Include more detailed nutritional information, rationale for recommendations, and guidance on adapting the plan as needed.'}
    
    {'' if 'visual' not in format_guidance else 'Design the plan to be highly visual with food images, simple icons, and minimal text. Use color coding to indicate foods that are encouraged (green), to be consumed in moderation (yellow), or to be limited/avoided (red).'}
    
    Return the plan in a well-formatted structure with clear sections.
    """
    
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
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a visual health educator specialized in creating accessible diabetes education materials."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    
    visual_guidance = response.choices[0].message.content.strip()
    return visual_guidance