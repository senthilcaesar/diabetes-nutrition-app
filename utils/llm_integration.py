import json
import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel

GEMINI_MODEL = "gemini-1.5-flash"  # Specify the model to use

# This module handles all Gemini API interactions for the diabetes nutrition plan application
def initialize_gemini_client():
    """Initialize Google API with the API key from Streamlit secrets."""
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai

def create_health_assessment_tools():
    """
    Create a structured tools schema for generating health assessments with the specified format.
    
    Returns:
        list: A list containing the function schema for health assessment
    """
    tools = [
        {
            "function_declarations": [
                {
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
            ]
        }
    ]
    
    return tools

def generate_health_assessment(user_data):
    """Generate a health assessment using Gemini API based on user health data."""
    prompt = create_health_assessment_prompt(user_data)
    
    # Initialize Gemini
    genai = initialize_gemini_client()
    
    # Get the tools schema
    tools = create_health_assessment_tools()
    
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
                        You are an expert endocrinologist specializing in personalized diabetes care and metabolic 
                        health assessment and provides endocrine consultations. You lead active clinical research programs in the fields of osteoporosis and obesity/metabolic diseases.
                        Your task is to transform patient data into actionable insights by analyzing all available patient data, suggesting diagnoses and generating care plans.
                        Please focus on diabetes management, identify potential risks and areas of concern, and recommend 
                        strategies for improvement. You must return your assessment in the exact structured format requested.
                        """
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
                    structured_assessment = function_call.args.to_dict()
                elif hasattr(function_call.args, '_asdict'):
                    structured_assessment = function_call.args._asdict()
                elif hasattr(function_call.args, '__dict__'):
                    structured_assessment = function_call.args.__dict__
                elif hasattr(function_call.args, '_pb'):
                    # Extract from _pb attribute which is a MessageMapContainer
                    pb_obj = function_call.args._pb
                    
                    # Access values directly from pb_obj
                    structured_assessment = {}
                    
                    # Extract the key fields we need from pb_obj
                    try:
                        for key, value in pb_obj.items():
                            # Convert each value to a usable form based on its string representation
                            str_value = str(value)
                            
                            # Process the string representation to get clean values
                            if 'string_value:' in str_value:
                                # For simple string values
                                extracted_value = str_value.split('string_value:')[1].strip()
                                structured_assessment[key] = extracted_value.strip('"')
                            else:
                                # For complex structures, keep as is for now
                                structured_assessment[key] = str_value
                        
                        # Construct a proper key_metrics_analysis object if it's in the data
                        if 'key_metrics_analysis' in structured_assessment:
                            # Extract the key metrics
                            metrics_str = structured_assessment['key_metrics_analysis']
                            
                            # Create a proper object
                            key_metrics = {
                                "fasting_glucose": "Not provided",
                                "postmeal_glucose": "Not provided",
                                "hba1c": "Not provided"
                            }
                            
                            # Extract fasting glucose if available
                            if "fasting_glucose" in metrics_str:
                                fg_parts = metrics_str.split("fasting_glucose")
                                if len(fg_parts) > 1:
                                    fg_value_parts = fg_parts[1].split("string_value:")
                                    if len(fg_value_parts) > 1:
                                        fg_value = fg_value_parts[1].split("}")[0].strip().strip('"')
                                        key_metrics["fasting_glucose"] = fg_value
                            
                            # Extract postmeal glucose if available
                            if "postmeal_glucose" in metrics_str:
                                pg_parts = metrics_str.split("postmeal_glucose")
                                if len(pg_parts) > 1:
                                    pg_value_parts = pg_parts[1].split("string_value:")
                                    if len(pg_value_parts) > 1:
                                        pg_value = pg_value_parts[1].split("}")[0].strip().strip('"')
                                        key_metrics["postmeal_glucose"] = pg_value
                            
                            # Extract hba1c if available
                            if "hba1c" in metrics_str:
                                hba_parts = metrics_str.split("hba1c")
                                if len(hba_parts) > 1:
                                    hba_value_parts = hba_parts[1].split("string_value:")
                                    if len(hba_value_parts) > 1:
                                        hba_value = hba_value_parts[1].split("}")[0].strip().strip('"')
                                        key_metrics["hba1c"] = hba_value
                            
                            # Update the structured assessment
                            structured_assessment['key_metrics_analysis'] = key_metrics
                        else:
                            # Create default key_metrics_analysis if missing
                            structured_assessment['key_metrics_analysis'] = {
                                "fasting_glucose": "Not provided",
                                "postmeal_glucose": "Not provided",
                                "hba1c": "Not provided"
                            }
                        
                        # Handle recommendations as an array if needed
                        if 'recommendations' in structured_assessment and isinstance(structured_assessment['recommendations'], str):
                            # Check if it looks like a list representation
                            if 'list_value' in structured_assessment['recommendations']:
                                # Extract individual recommendations
                                recommendations = []
                                rec_str = structured_assessment['recommendations']
                                
                                # Extract all string values
                                parts = rec_str.split('string_value:')
                                for i in range(1, len(parts)):
                                    rec_value = parts[i].split('"')[1]
                                    recommendations.append(rec_value)
                                
                                # Update with extracted list
                                structured_assessment['recommendations'] = recommendations if recommendations else ["No specific recommendations available"]
                            else:
                                # Convert to a list with a single item
                                structured_assessment['recommendations'] = [structured_assessment['recommendations']]
                        
                        # Add default fields if missing
                        if 'summary' not in structured_assessment:
                            structured_assessment['summary'] = "Assessment unavailable"
                        if 'diabetes_management_evaluation' not in structured_assessment:
                            structured_assessment['diabetes_management_evaluation'] = "Evaluation unavailable"
                        if 'potential_health_risks' not in structured_assessment:
                            structured_assessment['potential_health_risks'] = "Risks assessment unavailable"
                        if 'suggested_diagnoses_and_care_plans' not in structured_assessment:
                            structured_assessment['suggested_diagnoses_and_care_plans'] = "Care plans unavailable"
                        if 'areas_of_concern' not in structured_assessment:
                            structured_assessment['areas_of_concern'] = "Areas of concern unavailable"
                        if 'recommendations' not in structured_assessment:
                            structured_assessment['recommendations'] = ["No specific recommendations available"]
                        if 'genetic_factors' not in structured_assessment:
                            structured_assessment['genetic_factors'] = {"summary": "No genetic data available"}
                        
                    except Exception as e:
                        print(f"Error extracting values from _pb: {e}")
                        
                        # Create a fallback structure
                        structured_assessment = {
                            "summary": "An error occurred while processing the assessment",
                            "diabetes_management_evaluation": "Evaluation unavailable due to processing error",
                            "key_metrics_analysis": {
                                "fasting_glucose": "See detailed assessment",
                                "postmeal_glucose": "See detailed assessment",
                                "hba1c": "See detailed assessment"
                            },
                            "potential_health_risks": "Risk assessment unavailable due to processing error",
                            "suggested_diagnoses_and_care_plans": "Care plans unavailable due to processing error",
                            "areas_of_concern": "Areas of concern unavailable due to processing error",
                            "recommendations": ["Please try again later or contact support"]
                        }
                else:
                    # Try direct attribute access
                    structured_assessment = {
                        "summary": getattr(function_call.args, "summary", "Summary unavailable"),
                        "diabetes_management_evaluation": getattr(function_call.args, "diabetes_management_evaluation", "Evaluation unavailable"),
                        "key_metrics_analysis": {
                            "fasting_glucose": "See detailed assessment",
                            "postmeal_glucose": "See detailed assessment",
                            "hba1c": "See detailed assessment"
                        },
                        "potential_health_risks": getattr(function_call.args, "potential_health_risks", "Risks assessment unavailable"),
                        "suggested_diagnoses_and_care_plans": getattr(function_call.args, "suggested_diagnoses_and_care_plans", "Care plans unavailable"),
                        "areas_of_concern": getattr(function_call.args, "areas_of_concern", "Areas of concern unavailable"),
                        "recommendations": getattr(function_call.args, "recommendations", ["No specific recommendations available"])
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
                    "potential_health_risks": "Assessment unavailable due to API error",
                    "suggested_diagnoses_and_care_plans": "Assessment unavailable due to API error",
                    "areas_of_concern": "Assessment unavailable due to API error",
                    "recommendations": ["Please try again later or contact support"]
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
                    "potential_health_risks": "See raw response below",
                    "suggested_diagnoses_and_care_plans": "See raw response below",
                    "areas_of_concern": "API response formatting issue",
                    "recommendations": ["See raw response below", text_response[:200] + "..."]
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
            "potential_health_risks": "Error processing response",
            "suggested_diagnoses_and_care_plans": "Error processing response",
            "areas_of_concern": "Error processing response",
            "recommendations": ["Please try again later or contact support"]
        }
    
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
    
    return prompt

def create_nutrition_plan_tools():
    """
    Create a structured tools schema for generating nutrition plans.
    
    Returns:
        list: A list containing the function schema for nutrition plan
    """
    tools = [
        {
            "function_declarations": [
                {
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
                            }
                        },
                        "required": ["introduction", "nutritional_overview", "recommended_foods", "foods_to_limit", "meal_plans"]
                    }
                }
            ]
        }
    ]
    
    return tools

def generate_nutrition_plan(user_data):
    """
    Generate a personalized nutrition plan using Gemini.
    
    Returns:
        tuple: (nutrition_plan, overview, meal_plan, recipes_tips) - complete plan and individual sections
    """
    prompt = create_nutrition_plan_prompt(user_data)
    
    # Initialize Gemini
    genai = initialize_gemini_client()
    
    # Get the tools schema
    tools = create_nutrition_plan_tools()
    
    # Create model instance
    model = GenerativeModel(GEMINI_MODEL)
    
    # Generate response with function calling
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": "You are a medical nutrition specialist with expertise in diabetes management. Create a personalized nutrition plan based on the provided health and socioeconomic data."
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
                        
                        # Set up default nutritional overview
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
                        
                        # Check if nutritional_overview is in extracted data
                        if "nutritional_overview" in extracted_data:
                            # Parse the string representation if needed
                            no_str = str(extracted_data["nutritional_overview"])
                            
                            # Extract calories if available
                            if "calories" in no_str:
                                try:
                                    calorie_parts = no_str.split("calories")
                                    if len(calorie_parts) > 1:
                                        calorie_str = calorie_parts[1].split(",")[0].strip(': ')
                                        try:
                                            calories = int(calorie_str)
                                            nutritional_overview["daily_caloric_target"]["calories"] = calories
                                        except ValueError:
                                            pass
                                except Exception:
                                    pass
                        
                        # Build structured plan
                        structured_plan = {
                            "nutritional_overview": nutritional_overview,
                            "introduction": extracted_data.get("introduction", "Welcome to your personalized nutrition plan"),
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
                                "day1": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                                "day2": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                                "day3": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"}
                            })
                        }
                    
                    except Exception as e:
                        print(f"Error iterating through _pb: {e}")
                        
                        # Use default structured plan
                        structured_plan = {
                            "nutritional_overview": {
                                "daily_caloric_target": {"calories": 2000, "explanation": "Based on your age, weight, height and activity level."},
                                "macronutrient_distribution": {
                                    "carbohydrates": {"percentage": 45, "grams": 225, "recommendations": "Focus on complex carbohydrates with fiber."},
                                    "protein": {"percentage": 25, "grams": 125, "recommendations": "Choose lean protein sources like chicken, fish, and plant proteins."},
                                    "fat": {"percentage": 30, "grams": 67, "recommendations": "Emphasize healthy unsaturated fats like avocados, nuts, and olive oil."}
                                },
                                "meal_structure": {
                                    "meal_frequency": "3-5 meals per day",
                                    "timing_recommendations": "Space meals 3-4 hours apart to help maintain stable blood sugar",
                                    "portion_guidance": "Use the plate method: ½ non-starchy vegetables, ¼ protein, ¼ carbohydrates"
                                }
                            },
                            "recommended_foods": {
                                "carbohydrates": ["Whole grains (brown rice, quinoa, oats)", "Legumes (beans, lentils)", "Sweet potatoes", "Whole grain bread"],
                                "proteins": ["Lean poultry", "Fish", "Tofu and tempeh", "Legumes", "Low-fat dairy"],
                                "fats": ["Avocados", "Nuts and seeds", "Olive oil", "Fatty fish"],
                                "vegetables": ["Leafy greens", "Broccoli", "Peppers", "Zucchini", "Cauliflower"],
                                "fruits": ["Berries", "Apples", "Citrus fruits", "Pears", "Cherries"],
                                "beverages": ["Water", "Unsweetened tea", "Black coffee", "Herbal tea"]
                            },
                            "foods_to_limit": [
                                {"food_category": "Sugary Foods", "reason": "Can cause blood sugar spikes", "alternatives": "Fresh fruit, especially berries"},
                                {"food_category": "Refined Carbohydrates", "reason": "Quickly raise blood glucose", "alternatives": "Whole grains and legumes"}
                            ],
                            "meal_plans": {
                                "day1": {
                                    "breakfast": "Overnight oats with berries and nuts",
                                    "lunch": "Grilled chicken salad with olive oil dressing",
                                    "dinner": "Baked fish with roasted vegetables and quinoa"
                                },
                                "day2": {
                                    "breakfast": "Vegetable omelet with whole grain toast",
                                    "lunch": "Bean and vegetable soup with side salad",
                                    "dinner": "Stir-fry with tofu and brown rice"
                                },
                                "day3": {
                                    "breakfast": "Greek yogurt with berries and nuts",
                                    "lunch": "Turkey and avocado wrap with vegetables",
                                    "dinner": "Lentil curry with vegetables and brown rice"
                                }
                            }
                        }
                else:
                    # Try accessing individual properties directly
                    # Extract nutritional overview
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
                    
                    # Build structured plan from individual properties
                    structured_plan = {
                        "nutritional_overview": nutritional_overview,
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
                            "day1": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                            "day2": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"},
                            "day3": {"breakfast": "Balanced breakfast", "lunch": "Balanced lunch", "dinner": "Balanced dinner"}
                        })
                    }
            except Exception as e:
                print(f"Error extracting args with attribute access: {e}")
                # Fallback to a basic structure if all methods fail
                structured_plan = {
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
    overview, meal_plan, recipes_tips = format_structured_nutrition_plan(structured_plan)
    
    # Also create a complete plan by combining all sections (for backward compatibility)
    nutrition_plan = overview + "\n" + meal_plan + "\n" + recipes_tips
    
    print(nutrition_plan)
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
    try:
        # SECTION 1: OVERVIEW
        overview = ""
            
        # Nutritional Overview section with chart icon
        overview += ""
        
        # Make sure required elements exist in the structured data
        if not structured_data:
            raise ValueError("Empty structured data")
            
        if "nutritional_overview" not in structured_data:
            raise ValueError("Missing nutritional_overview")
            
        # Daily Caloric Target
        if "daily_caloric_target" not in structured_data["nutritional_overview"]:
            raise ValueError("Missing daily_caloric_target")
            
        caloric = structured_data["nutritional_overview"]["daily_caloric_target"]
        overview += f"### 🔥 Daily Caloric Target: {caloric.get('calories', 2000)} calories\n\n"
        overview += f"{caloric.get('explanation', 'No explanation provided')}\n\n"
    
        # Macronutrient Distribution with visualization-like formatting
        overview += "### 🥗 Macronutrient Distribution\n\n"
        
        if "macronutrient_distribution" not in structured_data["nutritional_overview"]:
            raise ValueError("Missing macronutrient_distribution")
            
        macro = structured_data["nutritional_overview"]["macronutrient_distribution"]
        
        # Create a visually appealing macronutrient table
        overview += "| Nutrient | Percentage | Grams |\n"
        overview += "|----------|------------|-------|\n"
        
        # Safely check for carbs, protein, fat with fallback values
        if "carbohydrates" in macro:
            carbs = macro["carbohydrates"]
            carb_percent = carbs.get("percentage", 45)
            carb_grams = carbs.get("grams", 225)
            carb_rec = carbs.get("recommendations", "Focus on complex carbohydrates")
        else:
            carb_percent = 45
            carb_grams = 225
            carb_rec = "Focus on complex carbohydrates (data missing)"
            
        if "protein" in macro:
            protein = macro["protein"]
            protein_percent = protein.get("percentage", 25)
            protein_grams = protein.get("grams", 125)
            protein_rec = protein.get("recommendations", "Focus on lean protein sources")
        else:
            protein_percent = 25
            protein_grams = 125
            protein_rec = "Focus on lean protein sources (data missing)"
            
        if "fat" in macro:
            fat = macro["fat"]
            fat_percent = fat.get("percentage", 30)
            fat_grams = fat.get("grams", 67)
            fat_rec = fat.get("recommendations", "Focus on healthy fats")
        else:
            fat_percent = 30
            fat_grams = 67
            fat_rec = "Focus on healthy fats (data missing)"
        
        # Add table rows with safe values
        overview += f"| **Carbohydrates** | {carb_percent}% | {carb_grams}g |\n"
        overview += f"| **Protein** | {protein_percent}% | {protein_grams}g |\n"
        overview += f"| **Fat** | {fat_percent}% | {fat_grams}g |\n\n"
        
        # Recommendations in styled boxes
        overview += f"**Carbohydrates:** {carb_rec}\n\n"
        overview += f"**Protein:** {protein_rec}\n\n"
        overview += f"**Fat:** {fat_rec}\n\n"
        
        # Meal Structure with clock icon
        overview += "### ⏰ Meal Structure and Timing\n\n"
        
        if "meal_structure" in structured_data["nutritional_overview"]:
            structure = structured_data["nutritional_overview"]["meal_structure"]
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

        if "recommended_foods" not in structured_data:
            raise ValueError("Missing recommended_foods")
            
        foods = structured_data["recommended_foods"]

        # Create a table for foods with headers
        overview += "| Category | Recommended Foods |\n"
        overview += "|----------|-------------------|\n"

        # Safely add food categories with fallbacks
        carbs = foods.get("carbohydrates", ["Whole grains", "Legumes", "Starchy vegetables"])
        proteins = foods.get("proteins", ["Lean meats", "Fish", "Tofu"])
        fats = foods.get("fats", ["Avocado", "Nuts", "Olive oil"])
        vegetables = foods.get("vegetables", ["Broccoli", "Spinach", "Peppers"])
        fruits = foods.get("fruits", ["Berries", "Apples", "Citrus"])
        beverages = foods.get("beverages", ["Water", "Herbal tea", "Black coffee"])
        
        # Safely join lists or handle single strings
        def safe_join(items):
            if isinstance(items, list):
                return ", ".join(items)
            elif isinstance(items, str):
                return items
            else:
                return "No recommendations available"
        
        # Add each category to table
        overview += f"| 🌾 **Carbohydrates** | {safe_join(carbs)} |\n"
        overview += f"| 🥩 **Proteins** | {safe_join(proteins)} |\n"
        overview += f"| 🥑 **Fats** | {safe_join(fats)} |\n"
        overview += f"| 🥦 **Vegetables** | {safe_join(vegetables)} |\n"
        overview += f"| 🍎 **Fruits** | {safe_join(fruits)} |\n"
        overview += f"| 🥤 **Beverages** | {safe_join(beverages)} |\n\n"
        
        overview += "</div>\n\n"
        
        # SECTION 2: MEAL PLAN
        meal_plan = ""
        
        # Sample Meal Plans with calendar icon
        meal_plan += ""

        if "meal_plans" not in structured_data:
            raise ValueError("Missing meal_plans")
            
        meal_plans = structured_data["meal_plans"]

        # Safe day meal getter
        def get_safe_meal_plan(day_num):
            day_key = f'day{day_num}'
            if day_key not in meal_plans:
                return {
                    "breakfast": f"Standard balanced breakfast for day {day_num} (data missing)",
                    "lunch": f"Standard balanced lunch for day {day_num} (data missing)",
                    "dinner": f"Standard balanced dinner for day {day_num} (data missing)"
                }
            return meal_plans[day_key]
            
        # Create tables for each day
        for day_num in range(1, 4):
            # Get meal plan with fallback
            day_meals = get_safe_meal_plan(day_num)
            
            meal_plan += f"## 🍽️ Day {day_num}\n\n"
            
            # Create table header
            meal_plan += "| Meal | Description |\n"
            meal_plan += "|------|-------------|\n"
            
            # Add meals with fallback values
            breakfast = day_meals.get('breakfast', f"Balanced breakfast for day {day_num}")
            lunch = day_meals.get('lunch', f"Balanced lunch for day {day_num}")
            dinner = day_meals.get('dinner', f"Balanced dinner for day {day_num}")
            
            # Add breakfast
            meal_plan += f"| 🌞 **Breakfast** | {breakfast} |\n"
            
            # Add morning snack if available
            if day_meals.get('morning_snack'):
                meal_plan += f"| 🥪 **Morning Snack** | {day_meals['morning_snack']} |\n"
            
            # Add lunch
            meal_plan += f"| 🍲 **Lunch** | {lunch} |\n"
            
            # Add afternoon snack if available
            if day_meals.get('afternoon_snack'):
                meal_plan += f"| 🍏 **Afternoon Snack** | {day_meals['afternoon_snack']} |\n"
            
            # Add dinner
            meal_plan += f"| 🍽️ **Dinner** | {dinner} |\n"
            
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
                
                # Get recipe properties with fallbacks
                name = recipe.get('name', 'Recipe')
                prep_time = recipe.get('prep_time', '30 minutes')
                ingredients = recipe.get('ingredients', 'Ingredients not provided')
                instructions = recipe.get('instructions', 'Instructions not provided')
                benefits = recipe.get('nutritional_benefits', 'Nutritional benefits not provided')
                
                # Add recipe details
                recipes_tips += f"### {name}\n\n"
                recipes_tips += f"**⏱️ Preparation Time:** {prep_time}\n\n"
                recipes_tips += f"**🛒 Ingredients:**\n{ingredients}\n\n"
                recipes_tips += f"**📝 Instructions:**\n{instructions}\n\n"
                recipes_tips += f"**💪 Nutritional Benefits:** {benefits}\n\n"
                recipes_tips += "</div>\n\n"
            
            recipes_tips += "---\n\n"

        # Foods to Limit section with stop sign icon
        recipes_tips += "# 🛑 Foods to Limit or Avoid\n\n"

        # Create table header
        recipes_tips += "| Food Category | Why to Limit | Better Alternatives |\n"
        recipes_tips += "|---------------|-------------|---------------------|\n"

        # Check for foods_to_limit with fallback
        if "foods_to_limit" in structured_data and structured_data["foods_to_limit"]:
            # Add each food item as a row in the table
            for item in structured_data["foods_to_limit"]:
                category = item.get('food_category', 'Processed foods')
                reason = item.get('reason', 'Can cause blood sugar spikes')
                alternatives = item.get('alternatives', 'Whole food alternatives')
                recipes_tips += f"| **{category}** | {reason} | {alternatives} |\n"
        else:
            # Add default foods to limit if missing
            recipes_tips += "| **Sugary Foods** | Can cause blood sugar spikes | Fresh fruit, berries |\n"
            recipes_tips += "| **Refined Carbs** | Rapid blood sugar elevation | Whole grains, legumes |\n"
            recipes_tips += "| **Fried Foods** | High in unhealthy fats | Baked, grilled, or steamed options |\n"

        recipes_tips += "---\n\n"
            
        
        # Blood Sugar Management with chart icon
        if "blood_sugar_management" in structured_data:
            recipes_tips += "# 📈 Blood Sugar Management Strategies\n\n"
            
            bsm = structured_data["blood_sugar_management"]
            
            # Get blood sugar management sections with fallbacks
            hypo = bsm.get('hypoglycemia_prevention', 'Carry fast-acting carbs for low blood sugar episodes')
            hyper = bsm.get('hyperglycemia_management', 'Stay hydrated and exercise regularly to help lower high blood sugar')
            timing = bsm.get('meal_timing_strategies', 'Eat meals at regular times to help maintain stable blood sugar')
            snacking = bsm.get('snack_recommendations', 'Choose snacks that combine protein and complex carbs')
            
            # Add blood sugar management sections
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 📉 Preventing Low Blood Sugar (Hypoglycemia)\n\n"
            recipes_tips += f"{hypo}\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 📈 Managing High Blood Sugar (Hyperglycemia)\n\n"
            recipes_tips += f"{hyper}\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### ⏰ Meal Timing Strategies\n\n"
            recipes_tips += f"{timing}\n\n"
            recipes_tips += "</div>\n\n"
            
            recipes_tips += "<div class='management-card'>\n\n"
            recipes_tips += "### 🥕 Smart Snacking\n\n"
            recipes_tips += f"{snacking}\n\n"
            recipes_tips += "</div>\n\n"
        
        return overview, meal_plan, recipes_tips
    except Exception as e:
        print(f"Error formatting nutrition plan: {e}")
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
    
    return prompt

def generate_visual_guidance(nutrition_plan, literacy_level, plan_complexity):
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
    
    # Initialize Gemini
    genai = initialize_gemini_client()
    
    # Create model instance
    model = GenerativeModel(GEMINI_MODEL)
    
    # Generate response
    try:
        response = model.generate_content(
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": "You are a visual health educator specialized in creating accessible diabetes education materials."
                        },
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            generation_config={"temperature": 0.3, "max_output_tokens": 1500}
        )
        
        visual_guidance = response.text
        return visual_guidance
    except Exception as e:
        print(f"Error generating visual guidance: {e}")
        print(f"Response structure: {response if 'response' in locals() else 'No response generated'}")
        # Return a fallback guidance
        return """
        # Visual Guidance (Error in generation)
        
        An error occurred while generating visual aids. Please try again later or contact support.
        
        In the meantime, consider using these general visual aids for diabetes education:
        
        1. **Plate Method Visual** - A plate divided into sections: half for non-starchy vegetables, quarter for protein, quarter for carbohydrates
        
        2. **Blood Sugar Curve** - A simple graph showing blood sugar levels after eating different types of foods
        
        3. **Portion Size Guide** - Common household items to represent appropriate portion sizes
        
        4. **Traffic Light Food System** - Green (eat freely), Yellow (eat in moderation), Red (limit/avoid)
        
        5. **Daily Schedule Visual** - Clock-based visualization of meal timing and medication schedules
        """