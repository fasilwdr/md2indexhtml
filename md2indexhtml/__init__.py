"""
md2indexhtml - Beautiful Markdown to HTML Converter for Odoo

A powerful tool that converts Markdown files to stunning HTML pages
using comprehensive Odoo 18.0 frontend styling classes from web.assets_frontend.min.css.

Features:
- Comprehensive Odoo styling with dictionary-based configuration
- Automatic image handling and copying
- Support for custom style configurations via JSON files
- Full HTML5 semantic element support
- Responsive design with Bootstrap-compatible classes
"""

from .converter import convert_md_to_html, __version__

__all__ = ["convert_md_to_html", "__version__"]
__author__ = "fasilwdr"
__description__ = "Beautiful Markdown to HTML converter with comprehensive Odoo frontend styling"