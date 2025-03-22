"""
Visualization module for the Diabetes Nutrition Plan application.
Contains functions for creating charts and visual representations.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Wedge, Polygon
import matplotlib.patheffects as path_effects


def create_enhanced_portion_guide(cultural_preferences=None, food_preferences=None, dietary_restrictions=None):
    """
    Create a visual portion guide for meal planning.
    
    Args:
        cultural_preferences (str, optional): Cultural food preferences
        food_preferences (list, optional): Food preferences
        dietary_restrictions (list, optional): Dietary restrictions
        
    Returns:
        matplotlib.figure.Figure: A figure containing the portion guide
    """
    try:
        # Create figure with a nice background
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Draw the plate
        plate = Circle((0.5, 0.5), 0.4, fill=True, color='#FFFFFF', ec='#333333', linewidth=2)
        ax.add_patch(plate)
        
        # Create the plate sections
        # Left half - vegetables
        veg_wedge = Wedge((0.5, 0.5), 0.4, 90, 270, color='#81c784', alpha=0.7)  # Green for vegetables
        ax.add_patch(veg_wedge)
        
        # Top right - proteins
        protein_wedge = Wedge((0.5, 0.5), 0.4, 270, 0, color='#ffb74d', alpha=0.7)  # Orange for proteins
        ax.add_patch(protein_wedge)
        
        # Bottom right - carbs
        carb_wedge = Wedge((0.5, 0.5), 0.4, 0, 90, color='#64b5f6', alpha=0.7)  # Blue for carbs
        ax.add_patch(carb_wedge)
        
        # Add section labels with icons
        ax.text(0.35, 0.6, "NON-STARCHY\nVEGETABLES\n(50%)", ha='center', va='center', fontweight='bold', color='#1b5e20')
        ax.text(0.70, 0.75, "PROTEINS\n(25%)", ha='center', va='center', fontweight='bold', color='#e65100')
        ax.text(0.75, 0.25, "CARBS\n(25%)", ha='center', va='center', fontweight='bold', color='#0d47a1')
        
        # Customize food examples based on user preferences and restrictions
        # Vegetables
        veg_examples = ["Broccoli", "Spinach", "Peppers", "Tomatoes", "Zucchini"]
        # Check if user has specified vegetable preferences
        if food_preferences and "Low vegetable intake" in food_preferences:
            veg_examples = ["Carrots", "Tomatoes", "Cucumber", "Corn", "Green Beans"]
        
        # Proteins
        protein_examples = ["Chicken", "Fish", "Beans", "Tofu", "Eggs", "Legumes", "Greek Yogurt"]
        # Customize protein examples based on dietary restrictions
        if dietary_restrictions:
            if "Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions:
                protein_examples = ["Tofu", "Beans", "Lentils", "Eggs", "Greek Yogurt", "Legumes", "Whole Grains"]
        
        # Carbs
        carb_examples = ["Brown rice", "Sweet potato", "Quinoa", "Whole grain bread"]
        # Customize carb examples based on preferences
        if dietary_restrictions and "gluten-free" in dietary_restrictions:
            carb_examples = ["Brown rice", "Sweet potato", "Quinoa", "Gluten-free oats"]
        
        # Column layout for examples
        for i, veg in enumerate(veg_examples[:5]):
            ax.text(0.15, 0.65 - i*0.06, f"• {veg}", fontsize=9, color='#1b5e20')
        
        for i, protein in enumerate(protein_examples):
            ax.text(0.52, 0.85 - i*0.05, f"• {protein}", fontsize=7, color='#e65100')
        
        for i, carb in enumerate(carb_examples[:4]):
            ax.text(0.52, 0.45 - i*0.06, f"• {carb}", fontsize=9, color='#0d47a1')
        
        # Add a helpful title with personalization
        title = "Diabetes-Friendly Portion Guide"
        if cultural_preferences:
            title = f"Diabetes-Friendly Portion Guide ({cultural_preferences} Focus)"
        
        ax.text(0.5, 0.95, title, ha='center', va='center', 
                fontsize=16, fontweight='bold', color='#333333')
        
        # Add a footnote
        ax.text(0.5, 0.05, "For optimal blood sugar management, follow this portion guide", 
                ha='center', va='center', fontsize=10, color='#555555', style='italic')
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        return fig
    except Exception as e:
        print(f"Error creating enhanced portion guide: {e}")
        return None


def create_enhanced_glucose_guide():
    """
    Create a blood glucose target range visualization.
    
    Returns:
        matplotlib.figure.Figure: A figure showing glucose target ranges
    """
    try:
        from matplotlib.patches import Rectangle, Polygon
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(10, 4), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Create a more attractive glucose meter visualization
        # Low range (red)
        ax.add_patch(Rectangle((0, 0.2), 0.3, 0.6, color='#ffcdd2', alpha=0.7))
        ax.text(0.15, 0.5, "LOW\n< 70 mg/dL\n\nSymptoms:\nShaking, sweating,\nconfusion, dizziness", 
                ha='center', va='center', fontsize=10, color='#c62828')
        
        # Target range (green)
        ax.add_patch(Rectangle((0.3, 0.2), 0.4, 0.6, color='#c8e6c9', alpha=0.7))
        ax.text(0.5, 0.5, "TARGET RANGE\n70-180 mg/dL\n\nGoal:\nStay in this range\nas much as possible", 
                ha='center', va='center', fontsize=12, fontweight='bold', color='#2e7d32')
        
        # High range (red)
        ax.add_patch(Rectangle((0.7, 0.2), 0.3, 0.6, color='#ffcdd2', alpha=0.7))
        ax.text(0.85, 0.5, "HIGH\n> 180 mg/dL\n\nSymptoms:\nThirst, fatigue,\nfrequent urination", 
                ha='center', va='center', fontsize=10, color='#c62828')
        
        # Add a meter-like pointer
        triangle_vertices = np.array([[0.5, 0.2], [0.47, 0.15], [0.53, 0.15]])
        meter = Polygon(triangle_vertices, color='#333333')
        ax.add_patch(meter)
        
        # Add a title
        ax.text(0.5, 0.9, "BLOOD GLUCOSE TARGET RANGES", ha='center', va='center', 
                fontsize=16, fontweight='bold', color='#333333')
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        return fig
    except Exception as e:
        print(f"Error creating enhanced glucose guide: {e}")
        return None


def create_foods_to_avoid_visual(dietary_restrictions=None):
    """
    Create a visual representation of foods to avoid with diabetes.
    
    Args:
        dietary_restrictions (list, optional): Dietary restrictions
        
    Returns:
        matplotlib.figure.Figure: A figure showing foods to avoid
    """
    try:
        # Create figure with a clean white background and optimized dimensions
        fig, ax = plt.subplots(figsize=(7, 3))
        
        # Set figure background color and reduce margins
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.1)
        
        # Add title - reduced font size
        ax.text(0.5, 0.88, "Foods to Limit or Avoid with Diabetes", 
                ha='center', fontsize=13, fontweight='bold', color='#d32f2f')
        
        # Define foods to avoid - customize based on user preferences
        foods = [
            "Sugary Drinks", 
            "White Bread", 
            "Fried Foods",
            "Processed Meats", 
            "Sweets & Desserts"
        ]
        
        # Customize based on dietary restrictions
        if dietary_restrictions:
            if "Vegetarian" in dietary_restrictions or "Vegan" in dietary_restrictions:
                foods[3] = "Processed Foods"  # Replace "Processed Meats" for vegetarians/vegans
        
        # Create more compact positions for items (in a single row)
        num_items = len(foods)
        x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
        y_position = 0.55  # Center position
        
        # Draw each food item with prohibition symbol - smaller size
        for i, (x, food) in enumerate(zip(x_positions, foods)):
            # Draw red circle - smaller size
            circle = plt.Circle((x, y_position), 0.05, fill=False, 
                            edgecolor='red', linewidth=1.5)
            ax.add_patch(circle)
            
            # Draw diagonal line for "no" symbol - smaller
            ax.plot([x-0.035, x+0.035], [y_position+0.035, y_position-0.035], 
                color='red', linewidth=1.5)
            
            # Add food label - smaller font
            ax.text(x, y_position-0.1, food, ha='center', fontsize=8, 
                fontweight='bold')
        
        # More compact explanation at bottom
        ax.text(0.5, 0.22, "These foods can cause rapid blood sugar spikes and worsen insulin resistance", 
            ha='center', fontsize=9, fontstyle='italic')
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Tight layout to reduce whitespace
        plt.tight_layout()
        
        return fig
    except Exception as e:
        print(f"Error creating foods to avoid visual: {e}")
        return None


def create_recommended_foods_visual(cultural_preferences=None, dietary_restrictions=None):
    """
    Create a visual representation of recommended foods for diabetes management.
    
    Args:
        cultural_preferences (str, optional): Cultural food preferences
        dietary_restrictions (list, optional): Dietary restrictions
        
    Returns:
        matplotlib.figure.Figure: A figure showing recommended foods
    """
    try:
        # Create figure with a tight layout and adjusted dimensions
        # Make the figure wider and shorter to fit horizontally on the page
        fig, ax = plt.subplots(figsize=(7, 3))
        
        # Set figure background color and reduce margins
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.1)
        
        # Add title with reduced font size
        title = "Recommended Foods for Blood Sugar Management"
        if cultural_preferences:
            title = f"Recommended Foods ({cultural_preferences} Options)"
        
        ax.text(0.5, 0.88, title, 
                ha='center', fontsize=13, fontweight='bold', color='#2e7d32')
        
        # Define recommended foods - customize based on user preferences
        foods = [
            "Whole Grains", 
            "Fresh Fruit", 
            "Protein",
            "Healthy Fats", 
            "Legumes"
        ]
        
        # Customize based on dietary or cultural preferences
        if dietary_restrictions:
            if "vegetarian" in dietary_restrictions or "Vegetarian" in dietary_restrictions:
                foods[2] = "Plant Protein"
            elif "vegan" in dietary_restrictions or "Vegan" in dietary_restrictions:
                foods[2] = "Plant Protein"
        
        # Create more compact positions for items (in a single row)
        num_items = len(foods)
        x_positions = [0.1 + i * 0.8/(num_items-1) for i in range(num_items)]
        y_position = 0.55  # Center position
        
        # Draw each food item with checkmark - smaller size
        for i, (x, food) in enumerate(zip(x_positions, foods)):
            # Draw green circle - smaller size
            circle = plt.Circle((x, y_position), 0.05, fill=True, 
                            facecolor='#c8e6c9', edgecolor='#2e7d32', linewidth=1.5)
            ax.add_patch(circle)
            
            # Draw checkmark - smaller
            ax.plot([x-0.025, x-0.008, x+0.03], [y_position-0.008, y_position-0.025, y_position+0.025], 
                color='#2e7d32', linewidth=1.5)
            
            # Add food label - smaller font
            ax.text(x, y_position-0.1, food, ha='center', fontsize=8, 
                fontweight='bold')
        
        # More compact explanation at bottom
        ax.text(0.5, 0.22, "These foods help maintain steady blood glucose levels and support overall health", 
            ha='center', fontsize=9, fontstyle='italic')
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Tight layout to reduce whitespace
        plt.tight_layout()
        
        return fig
    except Exception as e:
        print(f"Error creating recommended foods visual: {e}")
        return None


def create_simple_glucose_chart(fasting_glucose, postmeal_glucose):
    """
    Create a simple bar chart for glucose levels with clear boundaries.
    
    Args:
        fasting_glucose (float): Fasting glucose level in mg/dL
        postmeal_glucose (float): Post-meal glucose level in mg/dL
        
    Returns:
        matplotlib.figure.Figure: A figure showing glucose levels
    """
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)  # Add some padding
    
    # Define ranges and colors
    ranges = ['Normal', 'Prediabetes', 'Diabetes']
    colors = ['#2ecc71', '#f1c40f', '#e74c3c']  # Green, Yellow, Red
    
    # Define threshold values
    fasting_thresholds = [70, 100, 126, 200]
    postmeal_thresholds = [70, 140, 200, 300]
    
    # Create x positions for bars
    x = np.arange(2)
    width = 0.6
    
    # Create background bars for ranges
    for i in range(3):
        # Fasting glucose range visualization
        ax.barh(x[0], fasting_thresholds[i+1] - fasting_thresholds[i], 
               left=fasting_thresholds[i], height=width, 
               color=colors[i], alpha=0.5, edgecolor='white', linewidth=1)
        
        # Postmeal glucose range visualization
        ax.barh(x[1], postmeal_thresholds[i+1] - postmeal_thresholds[i], 
               left=postmeal_thresholds[i], height=width, 
               color=colors[i], alpha=0.5, edgecolor='white', linewidth=1)
    
    # Add values as vertical lines
    ax.axvline(x=fasting_glucose, ymin=0.25, ymax=0.45, color='black', linewidth=2)
    ax.axvline(x=postmeal_glucose, ymin=0.55, ymax=0.75, color='black', linewidth=2)
    
    # Add text for actual values
    ax.text(fasting_glucose, x[0] - 0.25, f"{fasting_glucose} mg/dL", 
           ha='center', va='center', fontweight='bold')
    ax.text(postmeal_glucose, x[1] + 0.25, f"{postmeal_glucose} mg/dL", 
           ha='center', va='center', fontweight='bold')
    
    # Set y-axis labels
    ax.set_yticks(x)
    ax.set_yticklabels(['Fasting\nGlucose', 'Post-meal\nGlucose'])
    
    # Set x-axis range and label
    ax.set_xlim(70, 300)
    ax.set_xlabel('Blood Glucose (mg/dL)')
    
    # Add title
    ax.set_title('Blood Glucose Levels', fontsize=14, fontweight='bold', pad=10)
    
    # Add a legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[0], alpha=0.5, label='Normal'),
        Patch(facecolor=colors[1], alpha=0.5, label='Prediabetes'),
        Patch(facecolor=colors[2], alpha=0.5, label='Diabetes')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    # Add grid lines
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Remove y-axis spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Make top and bottom spines visible and thicker for better boundary
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['top'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1)
    
    plt.tight_layout()
    
    return fig


def create_simple_hba1c_chart(hba1c):
    """
    Create a simple gauge chart for HbA1c with clear boundaries.
    
    Args:
        hba1c (float): HbA1c level in percentage
        
    Returns:
        matplotlib.figure.Figure: A figure showing HbA1c level
    """
    from matplotlib.patches import Patch
    
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2) 
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.25)  # Add some padding
    
    # Define ranges and colors
    ranges = [(4.0, 5.6), (5.7, 6.4), (6.5, 8.0), (8.1, 10.0)]
    colors = ['#2ecc71', '#f1c40f', '#3498db', '#e74c3c']  # Green, Yellow, Blue, Red
    labels = ['Normal', 'Prediabetes', 'Target with Diabetes', 'High Risk']
    
    # Create horizontal bars for each range
    for i, (start, end) in enumerate(ranges):
        ax.barh(0, end - start, left=start, height=0.5, 
               color=colors[i], alpha=0.7, edgecolor='white', linewidth=1)
    
    # Add marker for the actual value
    ax.axvline(x=hba1c, ymin=0.25, ymax=0.75, color='black', linewidth=2)
    
    # Add text for the value
    ax.text(hba1c, 0.7, f"{hba1c}%", ha='center', va='center', 
           fontsize=14, fontweight='bold')
    
    # Set x-axis range and ticks
    ax.set_xlim(4, 10)
    ax.set_xticks([4, 5, 6, 7, 8, 9, 10])
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Add title
    ax.set_xlabel('HbA1c (%)')
    
    # Add a legend
    legend_elements = [
        Patch(facecolor=colors[0], alpha=0.7, label=f'{labels[0]} ({ranges[0][0]}-{ranges[0][1]}%)'),
        Patch(facecolor=colors[1], alpha=0.7, label=f'{labels[1]} ({ranges[1][0]}-{ranges[1][1]}%)'),
        Patch(facecolor=colors[2], alpha=0.7, label=f'{labels[2]} ({ranges[2][0]}-{ranges[2][1]}%)'),
        Patch(facecolor=colors[3], alpha=0.7, label=f'{labels[3]} ({ranges[3][0]}%+)')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.8, -0.25), ncol=1)
    
    # Add grid
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Make all spines visible for a clear boundary
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)
    
    plt.tight_layout()
    
    return fig


def create_simple_bmi_chart(bmi):
    """
    Create a simple bar chart for BMI with clear boundaries.
    
    Args:
        bmi (float): Body Mass Index
        
    Returns:
        matplotlib.figure.Figure: A figure showing BMI categories
    """
    from matplotlib.patches import Patch
    
    # Create figure with a border
    fig, ax = plt.subplots(figsize=(12, 5), facecolor='white', edgecolor='#cccccc', linewidth=2)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.25)  # Add some padding
    
    # Define BMI categories and colors
    categories = ['Underweight', 'Normal', 'Overweight', 'Obese I', 'Obese II', 'Obese III']
    ranges = [(0, 18.4), (18.5, 24.9), (25, 29.9), (30, 34.9), (35, 39.9), (40, 50)]
    colors = ['#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#9b59b6']
    
    # Create horizontal bars for each BMI category
    for i, ((start, end), color) in enumerate(zip(ranges, colors)):
        ax.barh(0, end - start, left=start, height=0.5, 
               color=color, alpha=0.7, edgecolor='white', linewidth=1)
        
        # Add category label in the middle of each section
        if end - start > 3:  # Only add text if there's enough space
            ax.text(start + (end - start)/2, 0, categories[i], 
                   ha='center', va='center', fontsize=9, color='black',
                   fontweight='bold')
    
    # Add a marker for the actual BMI value
    ax.axvline(x=bmi, ymin=0.25, ymax=0.75, color='black', linewidth=2)
    
    # Add text for the BMI value
    ax.text(bmi, 0.7, f"BMI: {bmi}", ha='center', va='center', 
           fontsize=12, fontweight='bold')
    
    # Set x-axis range and label
    ax.set_xlim(0, 50)
    ax.set_xlabel('Body Mass Index (BMI)')
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    # Add a grid
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Make all spines visible for a clear boundary
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1)
    
    # Add a legend showing the categories and their ranges
    legend_elements = []
    for i, ((start, end), color, category) in enumerate(zip(ranges, colors, categories)):
        legend_elements.append(
            Patch(facecolor=color, alpha=0.7, label=f'{category} ({start}-{end})')
        )
    
    # Place legend below the chart
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.8, -0.30), ncol=2)
    
    plt.tight_layout()
    
    return fig


def create_health_metrics_visualizations(health_data):
    """
    Create visualizations for key health metrics.
    
    Args:
        health_data (dict): Dictionary containing user health information
        
    Returns:
        tuple: Three figures for glucose, HbA1c, and BMI visualizations
    """
    # Extract health metrics
    fasting_glucose = health_data.get('fasting_glucose', 0)
    postmeal_glucose = health_data.get('postmeal_glucose', 0)
    hba1c = health_data.get('hba1c', 0)
    bmi = health_data.get('bmi', 0)
    
    # Create figures for each metric
    glucose_fig = create_simple_glucose_chart(fasting_glucose, postmeal_glucose)
    hba1c_fig = create_simple_hba1c_chart(hba1c)
    bmi_fig = create_simple_bmi_chart(bmi)
    
    return glucose_fig, hba1c_fig, bmi_fig


