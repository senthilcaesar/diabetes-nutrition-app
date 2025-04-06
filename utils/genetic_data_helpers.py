"""
Helper functions for processing genetic nutrition data from API responses.
These functions support the genetic_llm_integration.py module by providing
utilities for parsing and managing MapComposite objects from the Gemini API.
"""

def create_default_genetic_nutritional_overview():
    """Create a default nutritional overview structure for genetic plans when data is missing."""
    return {
        "daily_caloric_target": {
            "calories": 2000,
            "explanation": "Based on your metabolic profile and genetic factors. Adjust based on your healthcare provider's guidance."
        },
        "macronutrient_distribution": {
            "carbohydrates": {
                "percentage": 45,
                "grams": 225,
                "recommendations": "Based on your genetic profile, focus on complex carbohydrates with low glycemic index like whole grains, legumes, and vegetables."
            },
            "protein": {
                "percentage": 25,
                "grams": 125,
                "recommendations": "Choose lean protein sources like chicken, fish, tofu, and legumes according to your genetic profile."
            },
            "fat": {
                "percentage": 30,
                "grams": 67,
                "recommendations": "Based on your genetic fat metabolism profile, emphasize healthy unsaturated fats while limiting saturated fats."
            }
        },
        "meal_structure": {
            "meal_frequency": "3-5 meals per day",
            "timing_recommendations": "Space meals 3-4 hours apart to help maintain stable blood sugar based on your genetic profile",
            "portion_guidance": "Use the plate method: ½ non-starchy vegetables, ¼ protein, ¼ carbohydrates"
        }
    }

def create_default_genetic_nutrition_plan():
    """Create a default genetic nutrition plan structure when data parsing fails."""
    return {
        "introduction": "This is a default genetic nutrition plan created when data parsing failed. Please consider regenerating your plan.",
        "nutritional_overview": create_default_genetic_nutritional_overview(),
        "genetic_optimization_strategies": {
            "carb_metabolism": "Based on your genetic profile, focus on complex carbohydrates with fiber to slow glucose absorption.",
            "fat_metabolism": "Your genetic profile suggests focusing on healthy unsaturated fats while limiting saturated fats.",
            "inflammation_response": "Consider adding anti-inflammatory foods to your diet based on your genetic profile.",
            "nutrient_processing": "Your genetic profile indicates potential need for specific nutrients.",
            "caffeine_metabolism": "Based on your genetics, moderate caffeine consumption is recommended."
        },
        "recommended_foods": {
            "carbohydrates": ["Whole grains", "Legumes", "Sweet potatoes", "Whole grain bread"],
            "proteins": ["Lean poultry", "Fish", "Tofu and tempeh", "Legumes", "Low-fat dairy"],
            "fats": ["Avocados", "Nuts and seeds", "Olive oil", "Fatty fish"],
            "vegetables": ["Leafy greens", "Broccoli", "Peppers", "Zucchini", "Cauliflower"],
            "fruits": ["Berries", "Apples", "Citrus fruits", "Pears"],
            "beverages": ["Water", "Unsweetened tea", "Black coffee"]
        },
        "foods_to_limit": [
            {"food_category": "Sugary Foods", "reason": "Can cause blood sugar spikes and inflammation", "alternatives": "Fresh fruit, especially berries"},
            {"food_category": "Refined Carbohydrates", "reason": "Your genetic profile shows sensitivity to refined carbs", "alternatives": "Whole grains and legumes"},
            {"food_category": "Processed Foods", "reason": "Often high in sodium and unhealthy fats", "alternatives": "Fresh, whole foods"}
        ],
        "meal_plans": {
            "day1": {
                "breakfast": "Overnight oats with berries and nuts",
                "morning_snack": "Apple with almond butter",
                "lunch": "Grilled chicken salad with olive oil dressing",
                "afternoon_snack": "Greek yogurt with walnuts",
                "dinner": "Baked fish with roasted vegetables and quinoa",
                "evening_snack": "Small piece of dark chocolate"
            },
            "day2": {
                "breakfast": "Vegetable omelet with whole grain toast",
                "morning_snack": "Small handful of mixed nuts",
                "lunch": "Bean and vegetable soup with side salad",
                "afternoon_snack": "Cottage cheese with berries",
                "dinner": "Turkey and vegetable stir-fry with brown rice",
                "evening_snack": "Celery with nut butter"
            },
            "day3": {
                "breakfast": "Greek yogurt parfait with fruit and nuts",
                "morning_snack": "Vegetables with hummus",
                "lunch": "Lentil salad with roasted vegetables",
                "afternoon_snack": "Hard-boiled egg and fruit",
                "dinner": "Grilled chicken with sweet potato and steamed vegetables",
                "evening_snack": "Small handful of berries"
            }
        },
        "genetic_food_recommendations": [
            {"category": "Omega-3 Sources", "reason": "Beneficial for your genetic inflammation profile", "foods": "Fatty fish, walnuts, flaxseeds"},
            {"category": "Antioxidant-Rich Foods", "reason": "Support your genetic response to oxidative stress", "foods": "Berries, colorful vegetables, green tea"},
            {"category": "Fiber Sources", "reason": "Optimal for your carbohydrate metabolism", "foods": "Legumes, whole grains, vegetables"}
        ],
        "blood_sugar_management": {
            "hypoglycemia_prevention": "Carry fast-acting carbs like glucose tablets. Never skip meals. Monitor blood sugar regularly.",
            "hyperglycemia_management": "Stay hydrated, exercise regularly, and follow your medication schedule as prescribed.",
            "meal_timing_strategies": "Eat meals at consistent times each day to help maintain stable blood sugar levels.",
            "snack_recommendations": "Choose snacks that combine protein and complex carbs for sustained energy."
        }
    }

def process_extracted_genetic_nutrition_data(extracted_data):
    """
    Process the extracted data from MapComposite objects into the standard genetic nutrition plan format.
    
    Args:
        extracted_data: Raw data extracted from the MapComposite object
        
    Returns:
        dict: A properly structured genetic nutrition plan
    """
    # Start with a default plan to ensure complete structure
    structured_plan = create_default_genetic_nutrition_plan()
    
    # Update with any available data from the extracted data
    if "introduction" in extracted_data:
        structured_plan["introduction"] = extracted_data["introduction"]
        
    # Process nutritional_overview if available
    if "nutritional_overview" in extracted_data:
        no_str = str(extracted_data["nutritional_overview"])
        
        # Try to extract the daily caloric target
        if "calories" in no_str and "daily_caloric_target" in structured_plan["nutritional_overview"]:
            try:
                # Extract calories value
                calorie_parts = no_str.split("calories")
                if len(calorie_parts) > 1:
                    calorie_value_part = calorie_parts[1].split(":")[1].strip() if ":" in calorie_parts[1] else calorie_parts[1].strip()
                    try:
                        calories = int(calorie_value_part.split(",")[0].strip())
                        structured_plan["nutritional_overview"]["daily_caloric_target"]["calories"] = calories
                    except (ValueError, IndexError):
                        pass
                        
                # Try to extract explanation
                if "explanation" in no_str:
                    explanation_parts = no_str.split("explanation")
                    if len(explanation_parts) > 1:
                        explanation_value = explanation_parts[1].split("string_value:")[1].split('"')[1] if 'string_value:' in explanation_parts[1] else explanation_parts[1].strip()
                        structured_plan["nutritional_overview"]["daily_caloric_target"]["explanation"] = explanation_value
            except Exception as e:
                print(f"Error extracting daily caloric target: {e}")
    
    # Process genetic_optimization_strategies if available
    if "genetic_optimization_strategies" in extracted_data:
        gos_str = str(extracted_data["genetic_optimization_strategies"])
        
        genetic_factors = ["carb_metabolism", "fat_metabolism", "inflammation_response", "nutrient_processing", "caffeine_metabolism"]
        for factor in genetic_factors:
            if factor in gos_str:
                try:
                    factor_parts = gos_str.split(factor)
                    if len(factor_parts) > 1:
                        factor_value = factor_parts[1].split("string_value:")[1].split('"')[1] if "string_value:" in factor_parts[1] else factor_parts[1].strip()
                        structured_plan["genetic_optimization_strategies"][factor] = factor_value
                except Exception as e:
                    print(f"Error extracting {factor}: {e}")
    
    # Process recommended_foods if available
    if "recommended_foods" in extracted_data:
        rf_str = str(extracted_data["recommended_foods"])
        
        food_categories = ["carbohydrates", "proteins", "fats", "vegetables", "fruits", "beverages"]
        for category in food_categories:
            if category in rf_str:
                try:
                    category_items = []
                    category_parts = rf_str.split(category)[1].split("list_value")[1] if "list_value" in rf_str.split(category)[1] else rf_str.split(category)[1]
                    
                    # Extract all string values for this category
                    item_parts = category_parts.split("string_value:")
                    for i in range(1, min(len(item_parts), 10)):  # Limit to 10 items to prevent parsing errors
                        item_value = item_parts[i].split('"')[1] if '"' in item_parts[i] else item_parts[i].strip()
                        category_items.append(item_value)
                        
                    if category_items:
                        structured_plan["recommended_foods"][category] = category_items
                except Exception as e:
                    print(f"Error extracting {category} foods: {e}")
    
    # Process meal_plans if available
    if "meal_plans" in extracted_data:
        mp_str = str(extracted_data["meal_plans"])
        
        for day_num in range(1, 4):
            day_key = f"day{day_num}"
            if day_key in mp_str:
                try:
                    day_plan = {}
                    day_part = mp_str.split(day_key)[1]
                    
                    # Extract meal components
                    meal_types = ["breakfast", "morning_snack", "lunch", "afternoon_snack", "dinner", "evening_snack"]
                    for meal in meal_types:
                        if meal in day_part:
                            meal_parts = day_part.split(meal)[1].split("string_value:")
                            if len(meal_parts) > 1:
                                meal_value = meal_parts[1].split('"')[1] if '"' in meal_parts[1] else meal_parts[1].strip().split('}')[0]
                                day_plan[meal] = meal_value
                    
                    # Update the structured plan if we found anything
                    if day_plan:
                        structured_plan["meal_plans"][day_key] = {**structured_plan["meal_plans"][day_key], **day_plan}
                except Exception as e:
                    print(f"Error extracting {day_key} meal plan: {e}")
    
    # Process genetic_food_recommendations if available
    if "genetic_food_recommendations" in extracted_data or "genetic_food_recs" in str(extracted_data):
        # Try multiple potential field names
        gfr_str = str(extracted_data.get("genetic_food_recommendations", extracted_data.get("genetic_food_recs", "")))
        
        try:
            recommendations = []
            
            # Extract from list representation
            if "category" in gfr_str and "reason" in gfr_str:
                category_parts = gfr_str.split("category")
                
                # Skip the first part (before the first "category")
                for i in range(1, min(len(category_parts), 10)):  # Limit to 10 items
                    try:
                        category_part = category_parts[i]
                        
                        # Extract category
                        category = ""
                        if "string_value:" in category_part:
                            category = category_part.split("string_value:")[1].split('"')[1]
                        
                        # Extract reason
                        reason = "Beneficial for your genetic profile"
                        if "reason" in category_part:
                            reason_part = category_part.split("reason")[1]
                            if "string_value:" in reason_part:
                                reason = reason_part.split("string_value:")[1].split('"')[1]
                        
                        # Extract foods
                        foods = "Various foods based on your genetic profile"
                        if "foods" in category_part:
                            foods_part = category_part.split("foods")[1]
                            if "string_value:" in foods_part:
                                foods = foods_part.split("string_value:")[1].split('"')[1]
                        
                        # Add to the list
                        if category:
                            recommendations.append({
                                "category": category,
                                "reason": reason,
                                "foods": foods
                            })
                    except Exception as e:
                        print(f"Error extracting genetic food recommendation #{i}: {e}")
            
            # Update the structured plan if we found anything
            if recommendations:
                structured_plan["genetic_food_recommendations"] = recommendations
        except Exception as e:
            print(f"Error extracting genetic food recommendations: {e}")
    
    # Process foods_to_limit if available
    if "foods_to_limit" in extracted_data:
        ftl_str = str(extracted_data["foods_to_limit"])
        
        try:
            foods_to_limit = []
            
            # Extract from list representation
            if "food_category" in ftl_str:
                category_parts = ftl_str.split("food_category")
                
                # Skip the first part (before the first "food_category")
                for i in range(1, min(len(category_parts), 10)):  # Limit to 10 items
                    try:
                        category_part = category_parts[i]
                        
                        # Extract food category
                        food_category = ""
                        if "string_value:" in category_part:
                            food_category = category_part.split("string_value:")[1].split('"')[1]
                        
                        # Extract reason
                        reason = "May negatively impact your genetic profile"
                        if "reason" in category_part:
                            reason_part = category_part.split("reason")[1]
                            if "string_value:" in reason_part:
                                reason = reason_part.split("string_value:")[1].split('"')[1]
                        
                        # Extract alternatives
                        alternatives = "See healthier options based on your genetic profile"
                        if "alternatives" in category_part:
                            alt_part = category_part.split("alternatives")[1]
                            if "string_value:" in alt_part:
                                alternatives = alt_part.split("string_value:")[1].split('"')[1]
                        
                        # Add to the list
                        if food_category:
                            foods_to_limit.append({
                                "food_category": food_category,
                                "reason": reason,
                                "alternatives": alternatives
                            })
                    except Exception as e:
                        print(f"Error extracting food to limit #{i}: {e}")
            
            # Update the structured plan if we found anything
            if foods_to_limit:
                structured_plan["foods_to_limit"] = foods_to_limit
        except Exception as e:
            print(f"Error extracting foods to limit: {e}")
    
    return structured_plan