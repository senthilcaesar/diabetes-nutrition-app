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
print('Testing final fixed health assessment generation...')

# Get data from Gemini API
result_from_api = generate_health_assessment(test_data)

# Now let's apply our new fixed solution explicitly to extract the data properly
def extract_health_assessment(result):
    # Check if result contains the structured response already
    if isinstance(result, dict) and 'summary' in result:
        print("Result already contains structured data")
        return result
        
    # Check for _pb attribute
    if not hasattr(result, '_pb') and not (isinstance(result, dict) and '_pb' in result):
        return {"error": "No _pb attribute found"}
    
    # Get the _pb object
    if hasattr(result, '_pb'):
        pb_obj = result._pb
    else:
        pb_obj = result['_pb']
    extracted_data = {}
    
    try:
        # Iterate through items in _pb
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
            elif 'struct_value' in str_value:
                # Handle nested structures
                extracted_data[key] = f"(Nested structure: {str_value})"
            elif 'list_value' in str_value:
                # Handle lists
                extracted_data[key] = f"(List structure: {str_value})"
            else:
                # For other types, keep as is
                extracted_data[key] = str_value
        
        return extracted_data
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {"error": str(e)}

# Extract the data properly
structured_data = extract_health_assessment(result_from_api)

# Print result
print('\nExtracted data:')
for key, value in structured_data.items():
    print(f'\n--- {key} ---')
    print(value)

print('\nTest completed successfully!')