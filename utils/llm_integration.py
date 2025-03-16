import json
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI

class DiabetesNutritionAI:
    """
    Class to handle interactions with the LLM for diabetes nutrition planning.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the nutrition AI with API credentials.
        
        Parameters:
        api_key (str): OpenAI API key
        model (str): Model to use for generation (default: gpt-4)
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def analyze_health_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze health metrics to identify nutritional needs.
        
        Parameters:
        health_data (dict): Dictionary of user health information
        
        Returns:
        dict: Analysis results with nutritional recommendations
        """
        prompt = self._create_health_analysis_prompt(health_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a medical nutrition specialist with expertise in diabetes management. Analyze the provided health data and identify key nutritional considerations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        analysis = response.choices[0].message.content.strip()
        
        # Extract structured information from the analysis
        analysis_dict = self._extract_structured_analysis(analysis)
        
        return analysis_dict
    
    def analyze_socioeconomic_factors(self, socio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze socioeconomic factors to identify adaptations needed.
        
        Parameters:
        socio_data (dict): Dictionary of user socioeconomic information
        
        Returns:
        dict: Analysis results with adaptation recommendations
        """
        prompt = self._create_socioeconomic_analysis_prompt(socio_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a social determinants of health expert specializing in healthcare accessibility. Analyze the provided socioeconomic data and identify key adaptations needed for an effective nutrition plan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1200
        )
        
        analysis = response.choices[0].message.content.strip()
        
        # Extract structured information from the analysis
        analysis_dict = self._extract_structured_analysis(analysis)
        
        return analysis_dict
    
    def generate_nutrition_plan(self, 
                                health_analysis: Dict[str, Any], 
                                socio_analysis: Dict[str, Any],
                                user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive nutrition plan based on analyses.
        
        Parameters:
        health_analysis (dict): Results from health data analysis
        socio_analysis (dict): Results from socioeconomic analysis
        user_data (dict): Combined user data
        
        Returns:
        dict: Complete nutrition plan
        """
        prompt = self._create_nutrition_plan_prompt(health_analysis, socio_analysis, user_data)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a medical nutrition specialist with expertise in creating personalized nutrition plans for individuals with diabetes. Create a comprehensive, culturally appropriate plan based on the provided analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2500
        )
        
        nutrition_plan = response.choices[0].message.content.strip()
        
        # Convert to structured plan with sections
        structured_plan = self._structure_nutrition_plan(nutrition_plan)
        
        return structured_plan
    
    def generate_visual_components(self, 
                                  nutrition_plan: Dict[str, Any], 
                                  literacy_level: str,
                                  complexity: str) -> List[Dict[str, Any]]:
        """
        Generate descriptions for visual components based on literacy level.
        
        Parameters:
        nutrition_plan (dict): The nutrition plan
        literacy_level (str): User's literacy level
        complexity (str): Plan complexity level
        
        Returns:
        list: List of visual component descriptions
        """
        prompt = self._create_visual_components_prompt(nutrition_plan, literacy_level, complexity)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a visual health educator specialized in creating accessible diabetes education materials. Create detailed descriptions for visual aids that would accompany a nutrition plan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        visual_descriptions = response.choices[0].message.content.strip()
        
        # Parse the descriptions into a structured format
        visual_components = self._parse_visual_descriptions(visual_descriptions)
        
        return visual_components
    
    def generate_cultural_adaptations(self, 
                                     base_plan: Dict[str, Any], 
                                     cultural_context: str,
                                     region: str) -> Dict[str, Any]:
        """
        Adapt the nutrition plan to be culturally appropriate.
        
        Parameters:
        base_plan (dict): The base nutrition plan
        cultural_context (str): Cultural background and food preferences
        region (str): Geographic region
        
        Returns:
        dict: Culturally adapted nutrition plan
        """
        prompt = self._create_cultural_adaptation_prompt(base_plan, cultural_context, region)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a cultural nutrition expert with deep knowledge of global food practices and diabetes management. Adapt the nutrition plan to be culturally appropriate while maintaining its effectiveness for diabetes management."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2000
        )
        
        adapted_plan = response.choices[0].message.content.strip()
        
        # Structure the adapted plan
        structured_adapted_plan = self._structure_nutrition_plan(adapted_plan)
        
        return structured_adapted_plan
    
    def generate_low_literacy_version(self, 
                                     nutrition_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a simplified version of the nutrition plan for low literacy users.
        
        Parameters:
        nutrition_plan (dict): The original nutrition plan
        
        Returns:
        dict: Simplified nutrition plan
        """
        prompt = self._create_low_literacy_prompt(nutrition_plan)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a health literacy expert specializing in creating accessible health information for individuals with low literacy. Simplify the nutrition plan while maintaining its essential information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1800
        )
        
        simplified_plan = response.choices[0].message.content.strip()
        
        # Structure the simplified plan
        structured_simplified_plan = self._structure_nutrition_plan(simplified_plan)
        
        return structured_simplified_plan
    
    def generate_meal_recipes(self, 
                             nutrition_plan: Dict[str, Any], 
                             cultural_context: str,
                             cooking_facilities: str,
                             prep_time: str,
                             num_recipes: int = 5) -> List[Dict[str, Any]]:
        """
        Generate simple, culturally appropriate recipes.
        
        Parameters:
        nutrition_plan (dict): The nutrition plan
        cultural_context (str): Cultural background and food preferences
        cooking_facilities (str): Available cooking equipment
        prep_time (str): Available time for meal preparation
        num_recipes (int): Number of recipes to generate
        
        Returns:
        list: List of recipe dictionaries
        """
        prompt = self._create_recipe_prompt(nutrition_plan, cultural_context, cooking_facilities, prep_time, num_recipes)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a culinary expert specializing in diabetes-friendly recipes that are culturally appropriate and practical for various cooking environments. Create simple, healthy recipes that align with the nutrition plan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Higher temperature for more creative recipes
            max_tokens=2500
        )
        
        recipes_text = response.choices[0].message.content.strip()
        
        # Parse recipes into structured format
        structured_recipes = self._parse_recipes(recipes_text)
        
        return structured_recipes
    
    # Private helper methods for creating prompts
    
    def _create_health_analysis_prompt(self, health_data: Dict[str, Any]) -> str:
        """Create a prompt for analyzing health data."""
        prompt = f"""
        Analyze the following health metrics for a person with diabetes and identify key nutritional considerations:
        
        ## Health Data
        - Age: {health_data.get('age')}
        - Gender: {health_data.get('gender')}
        - Weight (kg): {health_data.get('weight')}
        - Height (cm): {health_data.get('height')}
        - BMI: {health_data.get('bmi')}
        - Activity Level: {health_data.get('activity_level')}
        - Diabetes Type: {health_data.get('diabetes_type')}
        - Blood Glucose Levels:
            - Fasting: {health_data.get('fasting_glucose')} mg/dL
            - Post-meal average: {health_data.get('postmeal_glucose')} mg/dL
        - HbA1c: {health_data.get('hba1c')}%
        - Dietary Restrictions: {health_data.get('dietary_restrictions')}
        - Current Medications: {health_data.get('medications')}
        - Other Health Conditions: {health_data.get('other_conditions')}
        
        Based on this data, provide a structured analysis of:
        1. Estimated daily calorie needs
        2. Recommended macronutrient distribution (carbs, protein, fat)
        3. Key nutritional priorities based on diabetes type and other health conditions
        4. Specific nutrients to emphasize or limit
        5. Recommendations for meal timing and frequency
        6. Considerations for physical activity in relation to nutrition
        
        Format your response as a structured analysis with clear sections and concise recommendations.
        """
        return prompt
    
    def _create_socioeconomic_analysis_prompt(self, socio_data: Dict[str, Any]) -> str:
        """Create a prompt for analyzing socioeconomic data."""
        prompt = f"""
        Analyze the following socioeconomic factors for creating an accessible and effective nutrition plan:
        
        ## Socioeconomic Factors
        - Location: {socio_data.get('location')}
        - Geographic Setting: {socio_data.get('geographic_setting')}
        - Income Level: {socio_data.get('income_level')}
        - Education Level: {socio_data.get('education_level')}
        - Literacy Level: {socio_data.get('literacy_level')}
        - Language Preferences: {socio_data.get('language_preferences')}
        - Access to Technology: {socio_data.get('technology_access')}
        - Access to Healthcare: {socio_data.get('healthcare_access')}
        - Local Food Availability: {socio_data.get('local_food_availability')}
        - Grocery Budget: {socio_data.get('grocery_budget')}
        - Cooking Facilities: {socio_data.get('cooking_facilities')}
        - Time for Meal Preparation: {socio_data.get('meal_prep_time')}
        - Family Size: {socio_data.get('family_size')}
        - Support System: {socio_data.get('support_system')}
        - Cultural Food Preferences: {socio_data.get('cultural_foods')}
        
        Based on these factors, provide a structured analysis of:
        1. Key adaptations needed for the nutrition plan to be accessible and effective
        2. Recommendations for presentation format based on literacy and technology access
        3. Practical considerations based on cooking facilities and meal preparation time
        4. Cultural and regional food adaptations
        5. Economic considerations and budget-friendly strategies
        6. Support system and how to leverage it for plan adherence
        
        Format your response as a structured analysis with clear sections and concise recommendations.
        """
        return prompt
    
    def _create_nutrition_plan_prompt(self, 
                                     health_analysis: Dict[str, Any], 
                                     socio_analysis: Dict[str, Any],
                                     user_data: Dict[str, Any]) -> str:
        """Create a prompt for generating a nutrition plan."""
        diabetes_type = user_data.get('diabetes_type', 'Type 2')
        format_guidance = user_data.get('format_guidance', 'balanced text and visuals')
        plan_complexity = user_data.get('plan_complexity', 'moderate')
        cultural_foods = user_data.get('cultural_foods', 'No specific cultural preferences')
        
        prompt = f"""
        Create a comprehensive, personalized nutrition plan for an individual with {diabetes_type} diabetes based on the following analyses:
        
        ## Health Analysis
        {json.dumps(health_analysis, indent=2)}
        
        ## Socioeconomic Adaptations
        {json.dumps(socio_analysis, indent=2)}
        
        ## Plan Specifications
        Please create a nutrition plan that includes:
        
        1. Daily caloric target and macronutrient distribution (carbs, protein, fat)
        2. Recommended meal structure (timing and composition)
        3. A 7-day meal plan with specific foods
        4. Simple recipe ideas that require minimal preparation
        5. Guidance on proper portion sizes using common household items as references
        6. Tips for eating out or in social situations
        7. Specific foods to avoid or limit
        8. Foods that can help stabilize blood sugar
        
        The plan should be:
        - Appropriate for {plan_complexity} complexity level
        - Formatted with {format_guidance} in mind
        - Culturally appropriate considering: {cultural_foods}
        - Practical considering the individual's living conditions and cooking facilities
        - Specifically designed to help manage diabetes
        
        Return the plan in a well-structured format with clear sections.
        """
        return prompt
    
    def _create_visual_components_prompt(self, 
                                        nutrition_plan: Dict[str, Any], 
                                        literacy_level: str,
                                        complexity: str) -> str:
        """Create a prompt for generating visual component descriptions."""
        plan_text = json.dumps(nutrition_plan, indent=2) if isinstance(nutrition_plan, dict) else nutrition_plan
        
        prompt = f"""
        Create detailed descriptions for visual aids to accompany the following nutrition plan:
        
        NUTRITION PLAN:
        {plan_text}
        
        The user has a {literacy_level} literacy level and the plan complexity is {complexity}.
        
        For each key concept in the nutrition plan, describe a simple, clear visual that could help communicate the information. These visual descriptions should:
        
        1. Focus on concrete representations of abstract concepts
        2. Use familiar objects, symbols, and scenarios
        3. Employ color coding for categorization (e.g., green for "good" foods, red for "avoid" foods)
        4. Include visual portion guides using common household objects
        5. Illustrate time-based concepts (meal timing, medication schedules)
        
        {'Include detailed visual descriptions that represent key information with minimal reliance on text.' if 'low' in literacy_level.lower() else 'Balance visual elements with text to reinforce key concepts.'}
        
        Provide 5-7 detailed visual descriptions covering the most important aspects of the nutrition plan.
        
        For each visual, provide:
        1. A clear title
        2. A detailed description of what the visual should look like
        3. The key message this visual is meant to convey
        """
        return prompt
    
    def _create_cultural_adaptation_prompt(self, 
                                          base_plan: Dict[str, Any], 
                                          cultural_context: str,
                                          region: str) -> str:
        """Create a prompt for cultural adaptation."""
        plan_text = json.dumps(base_plan, indent=2) if isinstance(base_plan, dict) else base_plan
        
        prompt = f"""
        Adapt the following nutrition plan to be culturally appropriate for someone from {cultural_context} living in {region}:
        
        ORIGINAL NUTRITION PLAN:
        {plan_text}
        
        Please transform this plan following these guidelines:
        
        1. Replace any Western-centric food examples with culturally appropriate alternatives
        2. Consider local food availability and traditional cooking methods
        3. Respect cultural food traditions while maintaining diabetes management principles
        4. Incorporate cultural beliefs and practices related to health and nutrition
        5. Use familiar local measurements and portion references
        6. Address common misconceptions about diabetes specific to this culture/region
        
        The adaptation should:
        - Maintain all essential health information and diabetes management principles
        - Feel culturally familiar and respectful to the reader
        - Acknowledge traditional foods and practices while providing healthy adaptations
        - Use culturally appropriate examples, analogies, and references
        
        For dietary recommendations specifically:
        - Suggest modifications to traditional dishes rather than elimination
        - Provide guidance on navigating cultural food events and celebrations
        - Recommend locally available alternatives to expensive imported health foods
        
        Return the adapted plan in a well-structured format with clear sections.
        """
        return prompt
    
    def _create_low_literacy_prompt(self, nutrition_plan: Dict[str, Any]) -> str:
        """Create a prompt for low literacy adaptation."""
        plan_text = json.dumps(nutrition_plan, indent=2) if isinstance(nutrition_plan, dict) else nutrition_plan
        
        prompt = f"""
        Adapt the following nutrition plan for someone with low literacy:
        
        ORIGINAL NUTRITION PLAN:
        {plan_text}
        
        Please transform this plan following these guidelines:
        
        1. Use extremely simple language (grade 3-4 reading level)
        2. Keep sentences very short (5-8 words per sentence)
        3. Use active voice only
        4. Replace any medical jargon with simple everyday terms
        5. Focus on concrete, actionable guidance rather than abstract concepts
        6. Use bullet points and numbered lists instead of paragraphs
        7. Include references to visual aids that could accompany the text
        8. Use familiar examples and analogies related to everyday life
        9. Repeat key points using slightly different wording
        
        The adapted plan should be:
        - Much shorter than the original
        - Focused only on the most essential information
        - Extremely clear with no ambiguity
        - Actionable with specific steps to follow
        - Suitable for someone who struggles with reading
        
        Return the adapted plan in a well-structured format with clear sections.
        """
        return prompt
    
    def _create_recipe_prompt(self, 
                             nutrition_plan: Dict[str, Any], 
                             cultural_context: str,
                             cooking_facilities: str,
                             prep_time: str,
                             num_recipes: int) -> str:
        """Create a prompt for generating recipes."""
        plan_text = json.dumps(nutrition_plan, indent=2) if isinstance(nutrition_plan, dict) else nutrition_plan
        
        prompt = f"""
        Create {num_recipes} simple, diabetes-friendly recipes that align with the following nutrition plan:
        
        NUTRITION PLAN:
        {plan_text}
        
        ## User Context
        - Cultural Food Preferences: {cultural_context}
        - Cooking Facilities: {cooking_facilities}
        - Meal Preparation Time: {prep_time}
        
        For each recipe, provide:
        1. A simple, descriptive title
        2. List of ingredients with measurements in common household units
        3. Alternative ingredients for items that might be hard to find
        4. Step-by-step instructions that are easy to follow
        5. Approximate preparation and cooking time
        6. Nutritional information per serving (calories, carbs, protein, fat)
        7. Tips for portion control
        
        The recipes should be:
        - Quick to prepare (under 30 minutes of active preparation time)
        - Require minimal cooking equipment
        - Use affordable, locally available ingredients
        - Culturally appropriate
        - Diabetes-friendly with controlled carbohydrate content
        
        Format each recipe clearly with all the required information.
        """
        return prompt
    
    # Helper methods for processing responses
    
    def _extract_structured_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Extract structured information from analysis text.
        
        In a production environment, you would implement a more robust approach,
        but for this example, we'll use a simple section-based extraction.
        """
        sections = {}
        current_section = "general"
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('##'):
                # This is a subsection header
                current_section = line.replace('#', '').strip().lower().replace(' ', '_')
                sections[current_section] = []
            elif line.startswith('#'):
                # This is a main section header
                current_section = line.replace('#', '').strip().lower().replace(' ', '_')
                sections[current_section] = []
            elif line:
                # This is content for the current section
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line)
        
        # Convert lists of lines to strings
        for section, content in sections.items():
            sections[section] = '\n'.join(content)
        
        return sections
    
    def _structure_nutrition_plan(self, plan_text: str) -> Dict[str, Any]:
        """
        Structure the nutrition plan into sections.
        """
        structured_plan = {}
        current_section = "overview"
        lines = plan_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('##'):
                # This is a subsection header
                current_section = line.replace('#', '').strip().lower().replace(' ', '_')
                structured_plan[current_section] = []
            elif line.startswith('#'):
                # This is a main section header
                current_section = line.replace('#', '').strip().lower().replace(' ', '_')
                structured_plan[current_section] = []
            elif line:
                # This is content for the current section
                if current_section not in structured_plan:
                    structured_plan[current_section] = []
                structured_plan[current_section].append(line)
        
        # Convert lists of lines to strings
        for section, content in structured_plan.items():
            structured_plan[section] = '\n'.join(content)
        
        return structured_plan
    
    def _parse_visual_descriptions(self, visual_text: str) -> List[Dict[str, Any]]:
        """
        Parse visual descriptions into a structured format.
        """
        visual_components = []
        current_component = None
        lines = visual_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('##'):
                # This is a visual component title
                if current_component:
                    visual_components.append(current_component)
                
                title = line.replace('#', '').strip()
                current_component = {"title": title, "description": "", "key_message": ""}
            elif line.startswith('#'):
                # This is a main section header
                if current_component:
                    visual_components.append(current_component)
                
                title = line.replace('#', '').strip()
                current_component = {"title": title, "description": "", "key_message": ""}
            elif "key message" in line.lower() or "key points" in line.lower():
                # This is the key message section
                if current_component:
                    current_component["key_message"] = line.split(":", 1)[1].strip() if ":" in line else line
            elif line and current_component:
                # This is content for the current component
                current_component["description"] += line + "\n"
        
        # Add the last component
        if current_component:
            visual_components.append(current_component)
        
        return visual_components
    
    def _parse_recipes(self, recipes_text: str) -> List[Dict[str, Any]]:
        """
        Parse recipes into a structured format.
        """
        recipes = []
        current_recipe = None
        current_section = None
        lines = recipes_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('##'):
                # This is a recipe title
                if current_recipe:
                    recipes.append(current_recipe)
                
                title = line.replace('#', '').strip()
                current_recipe = {
                    "title": title,
                    "ingredients": [],
                    "instructions": [],
                    "prep_time": "",
                    "cook_time": "",
                    "nutritional_info": {},
                    "tips": []
                }
                current_section = None
            elif line.lower().startswith('ingredients'):
                current_section = "ingredients"
            elif line.lower().startswith('instructions') or line.lower().startswith('directions'):
                current_section = "instructions"
            elif line.lower().startswith('preparation time') or line.lower().startswith('prep time'):
                current_section = "prep_time"
                if ":" in line:
                    current_recipe["prep_time"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith('cooking time') or line.lower().startswith('cook time'):
                current_section = "cook_time"
                if ":" in line:
                    current_recipe["cook_time"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith('nutritional information'):
                current_section = "nutritional_info"
            elif line.lower().startswith('tips'):
                current_section = "tips"
            elif line and current_recipe and current_section:
                # Add content to the current section
                if current_section == "ingredients" and line[0].isdigit() or line[0] == '-':
                    current_recipe["ingredients"].append(line.lstrip('- '))
                elif current_section == "instructions" and line[0].isdigit() or line[0] == '-':
                    current_recipe["instructions"].append(line.lstrip('- '))
                elif current_section == "nutritional_info":
                    if ":" in line:
                        key, value = line.split(":", 1)
                        current_recipe["nutritional_info"][key.strip().lower()] = value.strip()
                elif current_section == "tips" and line[0].isdigit() or line[0] == '-':
                    current_recipe["tips"].append(line.lstrip('- '))
        
        # Add the last recipe
        if current_recipe:
            recipes.append(current_recipe)
        
        return recipes