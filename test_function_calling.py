import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os
import json

print("Testing Gemini API with function calling...")

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
        
        # Test different ways to access the args
        print("\nTrying different methods to access args:")
        
        if hasattr(function_call.args, 'to_dict'):
            print("Method 1 (to_dict) works!")
            args = function_call.args.to_dict()
            print(f"Args via to_dict(): {args}")
        else:
            print("Method 1 (to_dict) not available")
            
        if hasattr(function_call.args, '_asdict'):
            print("Method 2 (_asdict) works!")
            args = function_call.args._asdict()
            print(f"Args via _asdict(): {args}")
        else:
            print("Method 2 (_asdict) not available")
            
        if hasattr(function_call.args, '__dict__'):
            print("Method 3 (__dict__) works!")
            args = function_call.args.__dict__
            print(f"Args via __dict__: {args}")
        else:
            print("Method 3 (__dict__) not available")
            
        # Try direct attribute access
        print("\nTrying direct attribute access:")
        try:
            name = getattr(function_call.args, "name", "unknown")
            age = getattr(function_call.args, "age", 0)
            occupation = getattr(function_call.args, "occupation", "unknown")
            print(f"Direct attributes: name={name}, age={age}, occupation={occupation}")
            print("Direct attribute access works!")
        except Exception as e:
            print(f"Direct attribute access failed: {e}")
            
        # Try JSON parsing
        print("\nTrying JSON parsing:")
        try:
            json_args = json.loads(str(function_call.args))
            print(f"JSON parsing result: {json_args}")
            print("JSON parsing works!")
        except Exception as e:
            print(f"JSON parsing failed: {e}")
            
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