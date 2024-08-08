# md2indexhtml/__init__.py

# Correct relative import
from .converter import convert_md_to_html

# Version of the package
__version__ = "0.1.0"

# Define what is available when the package is imported
__all__ = ["convert_md_to_html"]
