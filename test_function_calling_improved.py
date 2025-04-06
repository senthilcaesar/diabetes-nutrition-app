import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os
import json
import inspect

print("Testing Gemini API with function calling (improved)...")

# Try to get API key from environment or Streamlit secrets
try:
    # First try environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    
    # If not in environment, try Streamlit secrets
    if not api_key and hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
        print("Using API key from Streamlit secrets")
    elif api_key:
        print("Using API key from environment")
    else:
        print("No API key found in environment or Streamlit secrets")
        api_key = "MISSING_API_KEY"  # This will cause an obvious error later
    
    # Configure the API
    genai.configure(api_key=api_key)
    print("Configured API. Testing function calling...")
    
    # Define a simple function schema
    tools = [
        {
            "function_declarations": [
                {
                    "name": "get_person_info",
                    "description": "Get information about a person",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string", 
                                "description": "The person's name"
                            },
                            "age": {
                                "type": "integer",
                                "description": "The person's age"
                            },
                            "occupation": {
                                "type": "string",
                                "description": "The person's job or occupation"
                            }
                        },
                        "required": ["name", "age"]
                    }
                }
            ]
        }
    ]
    
    # Create model and generate response with function calling
    model = GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(
        "Please provide information about a fictional person named John who is 35 years old and works as a software engineer.",
        generation_config={"temperature": 0.2},
        tools=tools,
        tool_config={"function_calling_config": {"mode": "any"}}
    )
    
    # Check if function calling was used
    if hasattr(response.candidates[0].content, 'parts') and hasattr(response.candidates[0].content.parts[0], 'function_call'):
        function_call = response.candidates[0].content.parts[0].function_call
        print("\nFunction calling successful!")
        print(f"Function name: {function_call.name}")
        print(f"Args type: {type(function_call.args)}")
        print(f"Args: {function_call.args}")
        
        # Examine the args object in detail
        print("\n=== DETAILED EXAMINATION OF ARGS OBJECT ===")
        
        # Get all attributes of the args object
        print("\nAll attributes of args object:")
        for attr in dir(function_call.args):
            if not attr.startswith('__'):
                print(f"- {attr}")
        
        # Check for _pb attribute specifically which we found in the previous test
        if hasattr(function_call.args, '_pb'):
            print("\nFound _pb attribute!")
            pb_obj = function_call.args._pb
            print(f"_pb type: {type(pb_obj)}")
            print(f"_pb contents: {pb_obj}")
            
            # Check if _pb has the fields we need
            print("\nExploring _pb contents:")
            if hasattr(pb_obj, 'name'):
                print(f"- Found name: {pb_obj.name}")
            if hasattr(pb_obj, 'age'):
                print(f"- Found age: {pb_obj.age}")
            if hasattr(pb_obj, 'occupation'):
                print(f"- Found occupation: {pb_obj.occupation}")
            
            # Try looping through fields if it's a container
            try:
                print("\nAttempting to iterate through _pb:")
                for key, value in pb_obj.items():
                    print(f"- {key}: {value}")
            except Exception as e:
                print(f"Iteration error: {e}")
                
                # Try alternative methods to get the fields
                print("\nTrying to get fields by examining _pb dir:")
                for attr in dir(pb_obj):
                    if not attr.startswith('__'):
                        try:
                            value = getattr(pb_obj, attr)
                            print(f"- {attr}: {value}")
                        except Exception as e:
                            print(f"- {attr}: (error accessing: {e})")
        
        # Try our fixed extraction approach
        print("\n=== TESTING OUR FIXED SOLUTION ===")
        try:
            # Try accessing individual fields
            if hasattr(function_call.args, '_pb'):
                pb_obj = function_call.args._pb
                
                # Try to extract values from pb_obj
                extracted_data = {}
                
                # Find all fields in pb_obj
                fields = []
                for field in dir(pb_obj):
                    if not field.startswith('_'):
                        fields.append(field)
                
                print(f"Found fields in _pb: {fields}")
                
                # Manually extract from string representation as last resort
                str_pb = str(pb_obj)
                print(f"String representation: {str_pb}")
                
                # Parse string representation to get values
                name = None
                age = None
                occupation = None
                
                if "name" in str_pb and "string_value" in str_pb:
                    name_parts = str_pb.split("'name': string_value: ")
                    if len(name_parts) > 1:
                        name_str = name_parts[1].split("\n")[0].strip('"')
                        name = name_str
                        
                if "age" in str_pb and "number_value" in str_pb:
                    age_parts = str_pb.split("'age': number_value: ")
                    if len(age_parts) > 1:
                        age_str = age_parts[1].split("\n")[0]
                        try:
                            age = int(age_str)
                        except:
                            age = float(age_str)
                            
                if "occupation" in str_pb and "string_value" in str_pb:
                    occupation_parts = str_pb.split("'occupation': string_value: ")
                    if len(occupation_parts) > 1:
                        occupation_str = occupation_parts[1].split("\n")[0].strip('"')
                        occupation = occupation_str
                
                print("\nExtracted values from string parsing:")
                print(f"Name: {name}")
                print(f"Age: {age}")
                print(f"Occupation: {occupation}")
                
                # This is our successful solution!
                if name is not None and age is not None:
                    print("\n✅ SOLUTION FOUND: String parsing of _pb attribute works!")
                
        except Exception as e:
            print(f"Error in our fixed solution: {e}")
            
    else:
        print("\nFunction calling was not used in the response")
        print("Full response:")
        print(response.text)
    
except Exception as e:
    print(f"\nError occurred: {e}")
    print("\nPossible issues:")
    print("1. Missing or invalid API key")
    print("2. Network connection issues") 
    print("3. Google Generative AI library issues")
    print("4. Function calling not supported on this model")