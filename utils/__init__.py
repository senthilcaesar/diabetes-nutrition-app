"""
Diabetes Nutrition Plan application package.
This file makes the directory a Python package to resolve import issues.
"""

# Import modules from utils to make them available when importing the package
from utils.data_processing import *
from utils.llm_integration import *
from utils.ui_components import *
from utils.visualization import *

# Set version
__version__ = '0.1.0'