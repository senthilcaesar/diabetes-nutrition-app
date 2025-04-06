import streamlit as st
import json
from utils.llm_integration import generate_health_assessment

# Create test data
test_data = {
    'age': 45,
    'gender': 'Male',
    'weight': 80,
    'height': 175,
    'bmi': 26.1,
    'activity_level': 'Moderate',
    'diabetes_type': 'Type 2',
    'fasting_glucose': 130,
    'postmeal_glucose': 170,
    'hba1c': 7.2,
    'medications': 'Metformin 500mg',
    'other_conditions': 'Hypertension',
    'dietary_restrictions': 'No dairy'
}

# Run test
print('Testing health assessment generation...')

# Generate health assessment
result = generate_health_assessment(test_data)

# Print result info
print('\nTest completed with result:')
print(f'Result type: {type(result)}')
print(f'Result keys: {result.keys() if isinstance(result, dict) else "Not a dictionary"}')

# Print each key-value in the result
if isinstance(result, dict):
    print('\nDetailed results:')
    for key, value in result.items():
        print(f'\n--- {key} ---')
        print(value)
        
print('\nTest completed successfully!')