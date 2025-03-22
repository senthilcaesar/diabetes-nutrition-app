"""
Data processing module for the Diabetes Nutrition Plan application.
Contains functions for preprocessing and validating user input data.
"""

def preprocess_health_data(health_data):
    """
    Preprocess and validate health data.
    
    Args:
        health_data (dict): Dictionary containing user health information
        
    Returns:
        dict: Processed health data with calculated metrics
    """
    processed_data = health_data.copy()
    
    # Convert values to appropriate types
    for key in ['age', 'weight', 'height']:
        if key in processed_data and processed_data[key]:
            processed_data[key] = float(processed_data[key])
    
    # Calculate BMI if height and weight are available
    if all(key in processed_data and processed_data[key] for key in ['weight', 'height']):
        height_m = processed_data['height'] / 100  # Convert cm to m
        processed_data['bmi'] = round(processed_data['weight'] / (height_m ** 2), 1)
    
    # Convert glucose values to float
    for key in ['fasting_glucose', 'postmeal_glucose', 'hba1c']:
        if key in processed_data and processed_data[key]:
            processed_data[key] = float(processed_data[key])
    
    return processed_data

def preprocess_socioeconomic_data(socio_data):
    """
    Preprocess and validate socioeconomic data.
    
    Args:
        socio_data (dict): Dictionary containing user socioeconomic information
        
    Returns:
        dict: Processed socioeconomic data with derived attributes
    """
    processed_data = socio_data.copy()
    
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

def combine_user_data(health_data, socio_data):
    """
    Combine processed health and socioeconomic data into a single dictionary.
    
    Args:
        health_data (dict): Processed health data
        socio_data (dict): Processed socioeconomic data
        
    Returns:
        dict: Combined user data
    """
    # Process both data sets
    processed_health_data = preprocess_health_data(health_data)
    processed_socio_data = preprocess_socioeconomic_data(socio_data)
    
    # Combine the data
    combined_data = {**processed_health_data, **processed_socio_data}
    
    return combined_data

def format_display_text(text, max_length=50):
    """
    Format text for display, truncating if too long.
    
    Args:
        text (str): Text to format
        max_length (int): Maximum length before truncating
        
    Returns:
        str: Formatted text
    """
    if not text:
        return "None"
        
    # Replace newlines with commas for display
    formatted_text = text.replace('\n', ', ').replace(',,', ',').strip(',')
    
    # Truncate if too long
    if len(formatted_text) > max_length:
        return formatted_text[:max_length] + "..."
    else:
        return formatted_text