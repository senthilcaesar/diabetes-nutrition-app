"""
Pages package for the Diabetes Nutrition Plan application.
Contains the different pages displayed in the application.
"""

# Import all page display functions for easier access
from app_pages.input_page import show_input_data_page
from app_pages.nutrition_plan_page import show_nutrition_plan
from app_pages.health_assessment_page import show_health_assessment
from app_pages.educational_resources_page import show_educational_resources

# Make utility functions available to pages
import sys
import os

# Add root directory to path to allow absolute imports from utils
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# Import utilities to make them available to page modules
try:
    from utils.data_processing import *
    from utils.llm_integration import *
    from utils.ui_components import *
    from utils.visualization import *
    # Add import for genetic modules
    from utils.genetic_processing import *
    from utils.genetic_ui_components import *
    from utils.genetic_llm_integration import *
except ImportError as e:
    # If imports fail, print informative message (won't appear in Streamlit UI)
    print(f"Warning: Could not import utility modules in pages/__init__.py: {e}")