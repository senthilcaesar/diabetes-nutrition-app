"""
Educational resources page for the Diabetes Nutrition Plan application.
Provides educational content about diabetes management.
"""

"""
Educational resources page for the Diabetes Nutrition Plan application.
Provides educational content about diabetes management.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Import visualization utilities if needed
try:
    # Try importing from the root directory
    from utils.visualization import create_glucose_chart, create_plate_method, create_activity_chart, create_glucose_log
    # If these functions exist in visualization.py, they will be imported
    # If not, we'll use our local implementations below
    USE_VISUALIZATION_MODULE = True
except ImportError:
    # If the visualization module isn't available or doesn't have these functions,
    # we'll use our local implementations
    USE_VISUALIZATION_MODULE = False

def create_glucose_chart():
    """Create a sample blood glucose chart."""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Sample data
    times = ["Fasting", "Before Lunch", "Before Dinner", "Bedtime"]
    target_min = [80, 80, 80, 100]
    target_max = [130, 130, 130, 140]
    
    # Plot target ranges
    for i in range(len(times)):
        ax.plot([i, i], [target_min[i], target_max[i]], 'g', linewidth=10, alpha=0.5)
    
    ax.set_xticks(range(len(times)))
    ax.set_xticklabels(times)
    ax.set_ylabel("Blood Glucose (mg/dL)")
    ax.set_title("Target Blood Glucose Ranges")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def create_plate_method():
    """Create a sample plate method visualization."""
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    
    # Data for the pie chart
    data = [50, 25, 25]
    labels = ['Non-starchy Vegetables', 'Protein', 'Carbohydrates']
    colors = ['#4CAF50', '#FFC107', '#2196F3']
    
    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
        data, 
        labels=labels, 
        colors=colors,
        autopct='%1.0f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'linewidth': 2}
    )
    
    ax.set_title('Diabetes Plate Method', fontsize=16)
    
    return fig

def create_activity_chart():
    """Create a sample activity benefits chart."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    activities = ["Walking", "Swimming", "Cycling", "Strength Training", "Yoga"]
    minutes = [30, 30, 30, 20, 20]
    
    # Create horizontal bars
    ax.barh(activities, minutes, color='#42A5F5')
    
    ax.set_xlabel("Recommended Minutes per Session")
    ax.set_title("Recommended Activities for Diabetes")
    ax.grid(True, linestyle='--', alpha=0.7, axis='x')
    
    return fig

def create_glucose_log():
    """Create a sample blood glucose log."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Sample data
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    fasting = [95, 102, 88, 110, 92]
    after_breakfast = [145, 160, 135, 172, 148]
    after_lunch = [138, 152, 140, 165, 130]
    after_dinner = [150, 145, 135, 180, 142]
    
    ax.plot(days, fasting, 'o-', label='Fasting')
    ax.plot(days, after_breakfast, 's-', label='After Breakfast')
    ax.plot(days, after_lunch, '^-', label='After Lunch')
    ax.plot(days, after_dinner, 'd-', label='After Dinner')
    
    # Add target range
    ax.axhspan(80, 130, alpha=0.2, color='green', label='Target Before Meals')
    ax.axhspan(130, 180, alpha=0.2, color='yellow', label='Target After Meals')
    
    ax.set_ylabel('Blood Glucose (mg/dL)')
    ax.set_title('Sample Blood Glucose Log')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    fig.autofmt_xdate()  # Rotate x-labels for better fit
    
    return fig

def show_educational_resources():
    """Display educational resources about diabetes nutrition."""
    st.header("Educational Resources")
    
    # Create tabs
    tab_names = [
        "Diabetes Basics", 
        "Food & Nutrition", 
        "Physical Activity", 
        "Monitoring", 
        "Cultural Adaptations"
    ]
    
    tabs = st.tabs(tab_names)
    
    st.markdown("---")
    
    # Educational content for each tab
    with tabs[0]:  # Diabetes Basics tab
        st.subheader("Understanding Diabetes")
        
        st.markdown("""
        #### What is Diabetes?
        Diabetes is a chronic condition that affects how your body turns food into energy. There are several types:
        
        - **Type 1 Diabetes**: The body doesn't produce insulin. This is usually diagnosed in children and young adults.
        - **Type 2 Diabetes**: The body doesn't use insulin properly. This is the most common type.
        - **Gestational Diabetes**: Develops during pregnancy in women who don't already have diabetes.
        - **Prediabetes**: Blood sugar is higher than normal but not high enough to be diagnosed as type 2 diabetes.
        
        #### How Diabetes Affects Your Body
        When you eat, your body turns food into glucose (sugar) that enters your bloodstream. Your pancreas releases insulin to help move glucose from the blood into cells for energy. With diabetes, either your body doesn't make enough insulin or can't use it effectively, leading to high blood sugar levels.
        
        #### Importance of Blood Sugar Management
        Consistently high blood sugar can damage your blood vessels and nerves over time, leading to complications like:
        - Heart disease
        - Kidney disease
        - Vision problems
        - Nerve damage
        - Foot problems
        
        Managing your blood sugar through diet, exercise, medication (if prescribed), and regular monitoring is essential for long-term health.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Blood Sugar Targets
            General targets for blood sugar levels:
            - **Before meals**: 80-130 mg/dL
            - **2 hours after meals**: Less than 180 mg/dL
            - **HbA1c**: Less than 7%
            
            Your healthcare provider may set different targets based on your individual situation.
            """)
        
        with col2:
            # Sample blood glucose chart
            st.pyplot(create_glucose_chart())
    
    with tabs[1]:  # Food & Nutrition tab
        st.subheader("Nutrition for Diabetes Management")
        
        st.markdown("""
        #### Key Principles of Diabetes Nutrition
        
        1. **Carbohydrate Management**: Carbohydrates have the most impact on blood sugar. Focus on:
           - Consistent carb intake at meals
           - Choosing complex carbs over simple sugars
           - Learning about portion sizes
        
        2. **Balanced Meals**: Include:
           - Healthy carbohydrates (whole grains, fruits, vegetables, legumes)
           - Lean proteins (fish, chicken, beans, tofu)
           - Healthy fats (olive oil, nuts, avocados)
           - Plenty of fiber
        
        3. **Plate Method**: A simple way to build balanced meals
           - ½ plate: non-starchy vegetables
           - ¼ plate: lean protein
           - ¼ plate: carbohydrates
           - Small amount of healthy fat
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Glycemic Index and Load
            The **Glycemic Index (GI)** measures how quickly foods raise blood sugar:
            - **Low GI (55 or less)**: Oatmeal, sweet potatoes, most fruits
            - **Medium GI (56-69)**: Brown rice, whole wheat bread
            - **High GI (70+)**: White bread, white rice, potatoes
            
            **Glycemic Load** considers both the GI and the amount of carbs in a serving, giving a more practical measure of a food's impact on blood sugar.
            """)
        
        with col2:
            # Sample plate method visual
            st.pyplot(create_plate_method())
    
    with tabs[2]:  # Physical Activity tab
        st.subheader("Physical Activity and Diabetes")
        
        st.markdown("""
        #### Benefits of Physical Activity for Diabetes
        
        Regular physical activity:
        - Lowers blood glucose by increasing insulin sensitivity
        - Helps maintain a healthy weight
        - Reduces cardiovascular disease risk
        - Improves mood and reduces stress
        - Strengthens muscles and bones
        
        #### Recommended Activity
        
        - **Aim for 150 minutes of moderate-intensity activity per week**
        - Spread activity throughout the week (e.g., 30 minutes, 5 days a week)
        - Include both aerobic exercise and strength training
        - Start slowly and gradually increase intensity
        
        #### Types of Physical Activity
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Aerobic Exercise**
            - Walking
            - Swimming
            - Cycling
            - Dancing
            
            **Strength Training**
            - Weight lifting
            - Resistance bands
            - Bodyweight exercises
            
            **Flexibility & Balance**
            - Yoga
            - Stretching
            - Tai Chi
            """)
        
        with col2:
            # Sample activity benefits chart
            st.pyplot(create_activity_chart())
        
        st.markdown("""
        #### Safety Tips
        
        - Check blood glucose before, during (for long sessions), and after activity
        - Carry fast-acting carbs (like glucose tablets) in case of low blood sugar
        - Stay hydrated
        - Wear proper footwear and inspect feet after activity
        - Start with low intensity and gradually increase
        - Talk to your healthcare provider before starting a new exercise program
        """)
    
    with tabs[3]:  # Monitoring tab
        st.subheader("Monitoring Blood Glucose")
        
        st.markdown("""
        #### Why Monitor Blood Glucose?
        
        Regular monitoring helps you:
        - Understand how food, activity, medication, and stress affect your blood sugar
        - Detect patterns and make adjustments to your management plan
        - Prevent or address high and low blood sugar episodes
        - Track your progress toward goals
        - Make informed decisions about food, activity, and medication
        
        #### When to Check Blood Glucose
        
        Common times to check include:
        - First thing in the morning (fasting)
        - Before meals
        - 1-2 hours after meals
        - Before and after physical activity
        - Before driving
        - When you feel symptoms of high or low blood sugar
        
        Your healthcare provider will recommend a specific schedule based on your needs.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Understanding Your Results
            
            General target ranges (may vary based on provider recommendations):
            
            - **Before meals**: 80-130 mg/dL
            - **1-2 hours after meals**: Less than 180 mg/dL
            - **Bedtime**: 100-140 mg/dL
            
            **HbA1c**: Measures average blood sugar over 2-3 months
            - Target for most adults with diabetes: Less than 7%
            
            #### Responding to Results
            
            **High Blood Sugar (Hyperglycemia)**
            - Drink water
            - Take medication as prescribed
            - Physical activity (if blood sugar isn't extremely high)
            - Check for illness or stress
            
            **Low Blood Sugar (Hypoglycemia)**
            - Follow the 15-15 Rule: Consume 15g of fast-acting carbs, wait 15 minutes, recheck
            - Examples of 15g carbs: 4 glucose tablets, 4 oz juice, 1 tbsp honey
            """)
        
        with col2:
            # Sample blood glucose log
            st.pyplot(create_glucose_log())
    
    with tabs[4]:  # Cultural Adaptations tab
        st.markdown("""#### Cultural Adaptations for Diabetes Management""")
        
        region = st.selectbox(
            "Select a Region for Cultural Adaptations",
            ["African Cuisine", "South Asian Cuisine", "Latin American Cuisine", "Middle Eastern Cuisine", "East Asian Cuisine"]
        )
        
        if region == "African Cuisine":
            st.markdown("""
            #### Adapting African Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Leafy greens (amaranth, collard greens, kale)
            - Legumes (black-eyed peas, chickpeas, lentils)
            - Lean proteins (fish, chicken, game meats)
            - Whole grains (millet, sorghum, brown rice)
            - Healthy fats (peanuts, avocados)
            
            **Modified Preparation Methods:**
            - Reduce palm oil and coconut oil; increase use of olive or peanut oil
            - Use less salt and bouillon cubes; flavor with herbs and spices
            - Bake, grill, or stew instead of deep frying
            - Cook starches until slightly firm ("al dente") to lower glycemic impact
            
            **Traditional Dishes - Healthier Versions:**
            - Jollof Rice: Use brown rice, increase vegetables, reduce oil
            - Fufu/Pounded Yam: Smaller portions, pair with vegetable soup
            - Stews: Increase vegetables, reduce oil, choose lean meats
            """)
        
        elif region == "South Asian Cuisine":
            st.markdown("""
            #### Adapting South Asian Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Legumes (lentils, chickpeas, beans)
            - Non-starchy vegetables (bitter gourd, okra, eggplant)
            - Lean proteins (fish, chicken, tofu)
            - Whole grains (brown rice, barley, millet)
            - Healthy fats (mustard oil, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Reduce ghee and coconut oil; use mustard oil or olive oil in moderation
            - Bake, grill, or steam instead of frying
            - Use less rice and more vegetables and proteins
            - Incorporate more bitter gourd, fenugreek, and cinnamon (help with glucose control)
            
            **Traditional Dishes - Healthier Versions:**
            - Dal: Emphasize this high-fiber, protein-rich dish
            - Chapati: Use whole wheat flour, make thinner
            - Curry: Increase vegetables, reduce oil, use low-fat yogurt instead of cream
            - Rice: Mix cauliflower rice with regular rice to reduce carbs
            """)
        
        elif region == "Latin American Cuisine":
            st.markdown("""
            #### Adapting Latin American Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Beans and legumes (black beans, pinto beans, lentils)
            - Vegetables (nopales, chayote, tomatoes, peppers)
            - Lean proteins (fish, chicken, lean cuts of beef)
            - Whole grains (brown rice, corn tortillas in moderation)
            - Healthy fats (avocados, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Use less lard and more olive oil or avocado oil
            - Bake, grill, or steam instead of frying
            - Use fresh ingredients rather than processed foods
            - Season with herbs and spices instead of salt
            
            **Traditional Dishes - Healthier Versions:**
            - Tacos: Use corn tortillas (smaller), increase vegetables, choose lean proteins
            - Rice: Mix cauliflower rice with regular rice, add vegetables
            - Beans: Keep these high-fiber foods, but prepare with less fat
            - Nopales (cactus): Emphasize this low-glycemic vegetable
            """)
        
        elif region == "Middle Eastern Cuisine":
            st.markdown("""
            #### Adapting Middle Eastern Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Legumes (chickpeas, lentils, fava beans)
            - Vegetables (eggplant, peppers, tomatoes, greens)
            - Lean proteins (fish, chicken, lean lamb)
            - Whole grains (bulgur, freekeh, whole wheat pita in moderation)
            - Healthy fats (olive oil, nuts, seeds)
            
            **Modified Preparation Methods:**
            - Use olive oil in moderation
            - Bake, grill, or roast instead of frying
            - Season with herbs and spices instead of salt
            - Reduce honey and sugar in recipes
            
            **Traditional Dishes - Healthier Versions:**
            - Hummus: High in fiber and protein, moderate portions
            - Tabbouleh: Emphasize this parsley-rich salad
            - Shawarma: Use lean meats, whole wheat wrap, plenty of vegetables
            - Stuffed vegetables: Include more lean protein, reduce rice
            """)
        
        elif region == "East Asian Cuisine":
            st.markdown("""
            #### Adapting East Asian Diets for Diabetes Management
            
            **Traditional Foods to Emphasize:**
            - Vegetables (bok choy, Chinese broccoli, mushrooms, seaweed)
            - Lean proteins (fish, tofu, chicken)
            - Legumes (edamame, tofu)
            - Whole grains (brown rice in moderation)
            - Healthy fats (sesame oil in moderation, nuts)
            
            **Modified Preparation Methods:**
            - Steam, stir-fry, or boil instead of deep frying
            - Use less oil in cooking
            - Reduce sodium (soy sauce, MSG)
            - Choose brown rice over white rice
            
            **Traditional Dishes - Healthier Versions:**
            - Stir-fries: Increase vegetable-to-meat ratio, use less oil
            - Rice: Mix cauliflower rice with regular rice, smaller portions
            - Soups: Clear broths with vegetables and lean proteins
            - Steam dishes: Emphasize steamed fish and vegetables
            """)
        
        st.markdown("""
        #### General Principles for Cultural Adaptation
        
        1. **Preserve Cultural Identity**: Modify traditional dishes rather than eliminate them
        2. **Use Traditional Wisdom**: Many cultures have traditional foods that are beneficial for diabetes
        3. **Focus on Cooking Methods**: Often changing preparation method is easier than changing the food itself
        4. **Portion Control**: Sometimes enjoying smaller amounts of traditional foods is the best approach
        5. **Community Involvement**: Include family and community in dietary changes for better support
        """)