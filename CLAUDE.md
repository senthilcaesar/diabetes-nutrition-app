# Development Prompts for Diabetes Nutrition App

## Core Application Setup

```
Create a Streamlit application for diabetes nutrition planning with these components:
1. A multi-page interface with: input collection, personalized nutrition plans, health assessment, and educational resources
2. OpenAI GPT-4 integration to generate personalized recommendations
3. Optional genetic data processing to enhance recommendations
4. Clear visualizations for health metrics and nutrition planning

The app should have:
- Clean, responsive UI with a sidebar for navigation
- Session state management to persist user data
- Proper error handling and loading states
- Type hints and clear documentation
```

## Project Structure Setup

```
Set up the project with this directory structure:
- app.py (main entry point)
- utils/ (utility modules)
  - __init__.py
  - data_processing.py
  - llm_integration.py
  - genetic_processing.py
  - genetic_llm_integration.py
  - ui_components.py
  - genetic_ui_components.py
  - visualization.py
- app_pages/ (application screens)
  - __init__.py
  - input_page.py
  - nutrition_plan_page.py
  - health_assessment_page.py
  - educational_resources_page.py
- example_data/ (sample genetic data)
  - sample_23andme.txt
- requirements.txt
```

## Main Application Entry Point

```
Create app.py as the main entry point with:
1. Streamlit configuration (wide layout, expanded sidebar)
2. Navigation system between four pages
3. Header component with application title
4. Custom CSS for styling the application
5. Main function to handle page switching based on sidebar selection

Use absolute imports to maintain clean architecture.
```

## UI Components Module

```
Create a UI components module (utils/ui_components.py) with:
1. Header display function with dynamic title based on genetic data availability
2. Custom CSS function with styles for:
   - Tabs, buttons, cards, and sections
   - Light/dark mode support
   - Responsive design adjustments
   - Custom message styling
3. Sidebar function with:
   - Navigation radio buttons
   - About section
   - Genetic data status indicator
4. Health data input function with:
   - Age, gender, weight, height, BMI calculator
   - Diabetes type, glucose levels, HbA1c
   - Activity level, dietary restrictions
   - Medications and health conditions
5. Socioeconomic data input function with:
   - Location, geographic setting, income level
   - Education and literacy level
   - Food availability and cooking facilities
   - Cultural preferences and family information
```

## LLM Integration Module

```
Create an OpenAI integration module (utils/llm_integration.py) with:
1. Client initialization function
2. Function calling tools JSON schema for:
   - Structured health assessments
   - Structured nutrition plans
3. Health assessment generation function with:
   - System prompt for an endocrinologist persona
   - User prompt builder with health metrics
   - Function calling for consistent output structure
4. Nutrition plan generation function with:
   - System prompt for medical nutrition specialist
   - User prompt with health and socioeconomic data
   - Function calling for structured meal plans
5. Visual guidance generation for creating supporting graphics
6. Result formatting functions for displaying the structured outputs
```

## Data Processing Module

```
Create a data processing module (utils/data_processing.py) with:
1. Input validation functions for health and socioeconomic data
2. Unit conversion functions (metric/imperial)
3. Session state management helpers
4. Function to combine health and socioeconomic data
5. Data anonymization for API transmission
6. User data persistence between sessions
```

## Genetic Data Processing Module

```
Create a genetic data processing module (utils/genetic_processing.py) with:
1. Constants for diabetes-relevant genetic markers:
   - TCF7L2 (rs7903146) - Carbohydrate metabolism
   - PPARG (rs1801282) - Insulin sensitivity
   - APOA2 (rs5082) - Saturated fat sensitivity
   - FTO (rs9939609) - Satiety response
   - MTHFR (rs1801133) - Folate processing
   - CYP1A2 (rs762551) - Caffeine metabolism
   - IL6 (rs1800795) - Inflammatory response
2. File parsers for common genetic data formats:
   - 23andMe format
   - Ancestry DNA format
   - VCF format
3. Genetic profile analysis functions for:
   - Carbohydrate metabolism analysis
   - Fat metabolism analysis
   - Vitamin metabolism analysis
   - Caffeine metabolism analysis
   - Inflammation response analysis
4. Summary generation function to explain genetic results
```

## Genetic LLM Integration

```
Create a genetic LLM integration module (utils/genetic_llm_integration.py) with:
1. Enhanced nutrition plan generation that incorporates genetic insights
2. Genetic health assessment generator
3. Prompt engineering to combine genetic data with health metrics
4. Custom function calling schemas for genetic-specific outputs
5. Explanation generation for genetic markers' impact on nutrition
```

## Input Page

```
Create the input data page (app_pages/input_page.py) with:
1. Tab interface with four sections:
   - Health Information
   - Socioeconomic Information
   - Genetic Information (optional)
   - Generate Plan
2. Progress tracking between sections
3. Data review function to summarize inputs
4. Plan generation workflow with:
   - Progress animation
   - Logic to use genetic data if available
   - API calls for nutrition plan generation
   - Success messages and navigation
5. Session state management for all inputs
```

## Nutrition Plan Page

```
Create the nutrition plan page (app_pages/nutrition_plan_page.py) with:
1. Tab interface for different plan sections:
   - Overview (calories, macros, meal structure)
   - Meal Plans (3-day sample plans)
   - Recipes & Tips (simple recipes, foods to limit)
2. Visualizations for:
   - Macronutrient distribution
   - Meal timing guidelines
   - Food category recommendations
3. Customized messaging based on user's:
   - Diabetes type
   - Socioeconomic constraints
   - Genetic profile (if available)
4. Print/save functionality
5. Explanations on how to implement the plan
```

## Health Assessment Page

```
Create the health assessment page (app_pages/health_assessment_page.py) with:
1. Current metrics display with:
   - Visual indicators for in/out of range values
   - Trend charts for key metrics
2. Health assessment generation functionality
3. Structured assessment display with sections:
   - Summary
   - Diabetes management evaluation
   - Key metrics analysis
   - Potential health risks
   - Suggested care plans
   - Areas of concern
   - Recommendations
   - Genetic factors (if data available)
4. Visual indicators of risk levels
5. Downloadable assessment report
```

## Educational Resources Page

```
Create an educational resources page (app_pages/educational_resources_page.py) with:
1. Categorized diabetes information:
   - Diabetes basics
   - Nutrition fundamentals
   - Exercise guidelines
   - Medication management
   - Complication prevention
2. Dynamic content based on user profile:
   - Diabetes type-specific information
   - Literacy-level appropriate materials
   - Culturally relevant resources
3. Interactive elements:
   - FAQ accordions
   - Glossary of terms
   - Quick reference guides
4. Links to reputable external resources
5. Downloadable educational materials
```

## Genetic UI Components

```
Create genetic UI components (utils/genetic_ui_components.py) with:
1. File upload widget for genetic data
2. Sample data option for demonstration
3. File validation and error handling
4. Genetic profile visualization:
   - Marker presence indicators
   - Metabolism sensitivity displays
   - Genotype impact explanations
5. Genetic data summary component
```

## Visualization Module

```
Create a visualization module (utils/visualization.py) with:
1. Health metric visualization functions:
   - Blood glucose charts
   - HbA1c trend visualization
   - BMI category display
2. Nutrition visualization functions:
   - Macronutrient pie charts
   - Meal plate composition guides
   - Portion size illustrations
3. Genetic data visualization:
   - Marker impact visualizations
   - Metabolism pathway illustrations
4. Customization based on literacy level
5. Exportable visualizations
```

## Requirements.txt

```
Create a requirements.txt file with these dependencies:
streamlit>=1.30.0
openai>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
Pillow>=9.0.0
python-dotenv>=0.20.0
scikit-learn>=1.0.0
```

## Sample Genetic Data

```
Create a sample genetic data file (example_data/sample_23andme.txt) with:
1. Standard 23andMe format header
2. Example entries for key diabetes-related markers:
   - rs7903146 (TCF7L2 gene)
   - rs1801282 (PPARG gene)
   - rs5082 (APOA2 gene)
   - rs9939609 (FTO gene)
   - rs1801133 (MTHFR gene)
   - rs762551 (CYP1A2 gene)
   - rs1800795 (IL6 gene)
3. Comment lines explaining the format
```

## Deployment Instructions

```
Add deployment instructions for:
1. Local development setup:
   - Python environment creation
   - Dependencies installation
   - API key configuration
2. Streamlit Cloud deployment:
   - GitHub repository setup
   - Secrets configuration
   - App URL sharing
3. Docker containerization option:
   - Dockerfile creation
   - Container build instructions
   - Environment variable configuration
```

## Code Style Guidelines

- **Imports**: Standard library first, third-party packages second, local modules last
- **Formatting**: Use snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Use triple quotes `"""` for all function and module documentation
- **Error Handling**: Use try/except blocks with specific exception types; use st.error() for user-facing errors
- **Naming**: Use descriptive variable names that clearly indicate purpose
- **Structure**: Maintain separation of concerns; UI components in utils/ui_components.py, data processing in utils/data_processing.py
- **Path Imports**: Use absolute imports (from utils.x import y) rather than relative imports
- **Comments**: Add comments for complex logic but prefer self-documenting code
- **Type Hints**: Add type hints to function parameters and return values for better code readability

## Build & Run Commands
- Run app: `streamlit run app.py`
- Install dependencies: `pip install -r requirements.txt`
- Update dependencies: `pip freeze > requirements.txt`