import streamlit as st
import google.generativeai as genai
from google.generativeai import GenerativeModel
import os

print("Trying to initialize Gemini API...")

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
    print("Configured API. Testing simple response...")
    
    # Create model and generate response
    model = GenerativeModel('gemini-2.5-pro-exp-03-25')
    response = model.generate_content('Hello! Can you respond with a simple greeting?')
    
    # Print results
    print("\nResponse received:")
    print(response.text)
    print("\nAPI test successful!")
    
except Exception as e:
    print(f"\nError occurred: {e}")
    print("\nPossible issues:")
    print("1. Missing or invalid API key")
    print("2. Network connection issues")
    print("3. Google Generative AI library issues")
    print("\nMake sure GEMINI_API_KEY is properly set in:")
    print("- Environment variables, or")
    print("- Streamlit secrets.toml file")
