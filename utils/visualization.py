import matplotlib as plt
import numpy as np
import io

def create_pictogram_food_guide(food_categories, literacy_level="low"):
    """
    Create a simple pictogram-based food guide suitable for low literacy users.
    
    Parameters:
    food_categories (dict): Dict with categories (eat often, sometimes, rarely) and foods
    literacy_level (str): Literacy level to adjust complexity
    
    Returns:
    BytesIO: Image buffer
    """
    if not food_categories:
        food_categories = {
            "Eat Often": ["Vegetables", "Lean proteins", "Whole grains"],
            "Eat Sometimes": ["Fruits", "Low-fat dairy", "Legumes"],
            "Eat Rarely": ["Sweets", "Fried foods", "White bread"]
        }
    
    # Define colors for each category
    colors = {
        "Eat Often": "#4CAF50",      # Green
        "Eat Sometimes": "#FFC107",  # Yellow
        "Eat Rarely": "#F44336"      # Red
    }
    
    # Create figure
    fig, axs = plt.subplots(len(food_categories), 1, figsize=(8, 10))
    
    for i, (category, foods) in enumerate(food_categories.items()):
        ax = axs[i]
        
        # Create colored background
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=colors[category], alpha=0.3))
        
        # Add category title
        ax.text(0.5, 0.85, category, ha='center', va='center', fontsize=16, 
                fontweight='bold', bbox=dict(facecolor=colors[category], alpha=0.8, boxstyle='round,pad=0.5'))
        
        # Add food items as simple text or icons
        spacing = 0.7 / len(foods)
        position = 0.7
        for food in foods:
            # In a real application, you might use icons here
            ax.text(0.5, position, food, ha='center', va='center', fontsize=14)
            position -= spacing
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_simple_meal_pairing_guide(meal_components, literacy_level="low"):
    """
    Create a visual guide for pairing meal components, suitable for low literacy users.
    
    Parameters:
    meal_components (dict): Dict with meal components and options
    literacy_level (str): Literacy level to adjust complexity
    
    Returns:
    BytesIO: Image buffer
    """
    if not meal_components:
        meal_components = {
            "Proteins": ["Chicken", "Fish", "Eggs", "Beans"],
            "Vegetables": ["Spinach", "Broccoli", "Carrots", "Peppers"],
            "Grains": ["Brown rice", "Quinoa", "Whole wheat bread"],
            "Fats": ["Avocado", "Olive oil", "Nuts"]
        }
    
    # Define colors
    colors = {
        "Proteins": "#F44336",    # Red
        "Vegetables": "#4CAF50",  # Green
        "Grains": "#FFC107",      # Yellow
        "Fats": "#2196F3"         # Blue
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw connecting lines between compatible items
    # This is simplified - in a real application, you'd have specific pairings
    
    # Hide axes
    ax.axis('off')
    
    # Set up the plate in the center
    center_circle = plt.Circle((0.5, 0.5), 0.2, fc='#E0E0E0')
    ax.add_patch(center_circle)
    ax.text(0.5, 0.5, "Healthy\nMeal", ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Position the food groups around the plate
    num_categories = len(meal_components)
    angle_step = 2 * np.pi / num_categories
    radius = 0.35  # Distance from center
    
    category_positions = {}
    
    for i, (category, foods) in enumerate(meal_components.items()):
        angle = i * angle_step
        x = 0.5 + radius * np.cos(angle)
        y = 0.5 + radius * np.sin(angle)
        
        # Draw a circle for the category
        category_circle = plt.Circle((x, y), 0.1, fc=colors[category], alpha=0.8)
        ax.add_patch(category_circle)
        
        # Add category label
        ax.text(x, y, category, ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Store position for connecting lines
        category_positions[category] = (x, y)
        
        # Add food items around the category
        num_foods = len(foods)
        food_radius = 0.15  # Distance from category to food items
        
        for j, food in enumerate(foods):
            food_angle = angle + (j - num_foods/2 + 0.5) * (angle_step * 0.5 / max(num_foods, 1))
            food_x = x + food_radius * np.cos(food_angle)
            food_y = y + food_radius * np.sin(food_angle)
            
            # Draw small circle for food item
            food_circle = plt.Circle((food_x, food_y), 0.05, fc=colors[category], alpha=0.5)
            ax.add_patch(food_circle)
            
            # Add food label
            ax.text(food_x, food_y, food, ha='center', va='center', fontsize=9)
            
            # Connect food to its category
            ax.plot([x, food_x], [y, food_y], color=colors[category], linestyle='-', alpha=0.5)
    
    # Connect each category to the center plate
    for (x, y) in category_positions.values():
        ax.plot([0.5, x], [0.5, y], 'k-', alpha=0.3)
    
    # Set the figure limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Title
    if literacy_level == "low":
        ax.text(0.5, 0.95, "Mix Foods To Make A Healthy Meal", ha='center', va='center', 
                fontsize=16, fontweight='bold')
    else:
        ax.text(0.5, 0.95, "Balanced Meal Component Guide", ha='center', va='center', 
                fontsize=16, fontweight='bold')
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_symptom_response_guide(symptoms_actions, literacy_level="low"):
    """
    Create a visual guide showing what to do when experiencing certain symptoms.
    
    Parameters:
    symptoms_actions (dict): Dict with symptoms and recommended actions
    literacy_level (str): Literacy level to adjust complexity
    
    Returns:
    BytesIO: Image buffer
    """
    if not symptoms_actions:
        symptoms_actions = {
            "Blood sugar too low\n(Below 70 mg/dL)": [
                "Eat 15g fast-acting carbs",
                "Wait 15 minutes",
                "Check blood sugar again",
                "If still low, repeat"
            ],
            "Blood sugar too high\n(Above 180 mg/dL)": [
                "Drink water",
                "Take medication if prescribed",
                "Check again in 2 hours",
                "Call doctor if still high"
            ],
            "Feeling dizzy or shaky": [
                "Sit down safely",
                "Check blood sugar",
                "Eat or drink something sweet",
                "Get help if not improving"
            ]
        }
    
    # Create figure
    num_symptoms = len(symptoms_actions)
    fig, axs = plt.subplots(num_symptoms, 1, figsize=(8, 4*num_symptoms))
    
    if num_symptoms == 1:
        axs = [axs]
    
    for i, (symptom, actions) in enumerate(symptoms_actions.items()):
        ax = axs[i]
        
        # Determine color based on severity
        if "low" in symptom.lower():
            color = "#FFC107"  # Yellow for low blood sugar
        elif "high" in symptom.lower():
            color = "#F44336"  # Red for high blood sugar
        else:
            color = "#2196F3"  # Blue for other symptoms
        
        # Add symptom as title
        ax.text(0.5, 0.9, symptom, ha='center', va='center', fontsize=14, 
                fontweight='bold', bbox=dict(facecolor=color, alpha=0.3, boxstyle='round,pad=0.5'))
        
        # Add numbered actions
        for j, action in enumerate(actions):
            y_pos = 0.8 - ((j+1) * 0.15)
            
            # Draw step number in a circle
            circle = plt.Circle((0.1, y_pos), 0.05, fc=color)
            ax.add_patch(circle)
            ax.text(0.1, y_pos, str(j+1), ha='center', va='center', fontweight='bold')
            
            # Add action text
            ax.text(0.25, y_pos, action, ha='left', va='center', fontsize=12)
        
        # Add a note for when to call healthcare provider
        if literacy_level == "low":
            ax.text(0.5, 0.1, "Call doctor if problem doesn't get better", ha='center', va='center', 
                    fontsize=10, style='italic', bbox=dict(facecolor='#E0E0E0', alpha=0.5, boxstyle='round'))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf
