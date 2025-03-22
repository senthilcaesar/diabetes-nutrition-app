# Personalized Diabetes Nutrition Plan

A Streamlit-based web application that generates personalized nutrition plans for individuals with diabetes based on their health metrics and socioeconomic context.

## Live Application

Access the live application at: [https://diabetes-nutrition-app.streamlit.app/](https://diabetes-nutrition-app.streamlit.app/)

## Project Structure

The application is organized in a modular structure to promote maintainability and separation of concerns:

```
diabetes_nutrition_plan/
│
├── app.py                # Main application entry point
│
├── utils/                # Utility modules
│   ├── data_processing.py    # Data validation and preprocessing functions
│   ├── llm_integration.py    # OpenAI API integration for generating content
│   ├── ui_components.py      # UI-related functions and components
│   └── visualization.py      # Functions for creating visualizations
│
└── app_pages/            # Application pages/screens
    ├── __init__.py                        # Package initialization
    ├── input_page.py                      # User input collection page
    ├── nutrition_plan_page.py             # Nutrition plan display page
    ├── health_assessment_page.py          # Health assessment page
    └── educational_resources_page.py      # Educational resources page
```

## Component Descriptions

### Main Application

- **app.py**: Entry point for the Streamlit application, handles navigation between different pages.

### Utility Modules

- **data_processing.py**: Contains functions for validating and preprocessing user data, ensuring it's in the right format for generating plans.

- **llm_integration.py**: Manages interactions with OpenAI's API to generate personalized health assessments, nutrition plans, and visual guidance descriptions.

- **ui_components.py**: Houses reusable UI components and functions for consistent interface elements across the application.

- **visualization.py**: Contains functions for creating visualizations like portion guides, glucose charts, and food recommendation visualizations.

### Application Pages

- **input_page.py**: Handles the collection of user health data and socioeconomic information through form inputs.

- **nutrition_plan_page.py**: Displays the AI-generated nutrition plan with tabs for different sections and visual guidance.

- **health_assessment_page.py**: Shows health metrics visualizations and displays the AI-generated health assessment.

- **educational_resources_page.py**: Provides educational content about diabetes management, nutrition, and cultural adaptations.

## Requirements

The application requires the following Python packages:

```
streamlit>=1.30.0
matplotlib>=3.7.0
numpy>=1.24.0
openai>=1.3.0
pandas>=2.0.0
scikit-learn>=1.0.0
```

Install all required packages using:

```bash
pip install -r requirements.txt
```

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/senthilcaesar/diabetes-nutrition-app.git
   cd diabetes-nutrition-app
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in Streamlit secrets.toml file:

   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Features

- Collects comprehensive health and socioeconomic data
- Generates personalized nutrition plans using AI
- Visualizes health metrics and nutrition guidelines
- Provides educational resources about diabetes management
- Adapts recommendations based on cultural preferences and socioeconomic factors

## Notes

- The application uses OpenAI's GPT-4 for generating personalized content
- Visualizations are created using Matplotlib
- The user interface is built with Streamlit

## Contact

For questions, support, or contributions, please contact:

- **Developer**: Senthil Palanivelu
- **Email**: senthilcaesar@gmail.com
- **GitHub**: [https://github.com/senthilcaesar](https://github.com/senthilcaesar)
- **LinkedIn**: [https://www.linkedin.com/in/senthilpalanivelu/](https://www.linkedin.com/in/senthilpalanivelu/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
