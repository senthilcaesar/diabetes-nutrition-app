"""
Diabetes Nutrition Plan application package.
This file makes the directory a Python package to resolve import issues.
"""

# Import modules from utils to make them available when importing the package
from utils.data_processing import *
from utils.llm_integration import *
from utils.ui_components import *
from utils.visualization import *

# Add imports for genetic modules
from utils.genetic_processing import *
from utils.genetic_ui_components import *
from utils.genetic_llm_integration import *

# Set version
__version__ = '0.2.0'  # Updated version to reflect genetic enhancements