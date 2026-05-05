"""
md2indexhtml - Section-type-aware Markdown to HTML converter for Odoo

Converts Markdown files to responsive HTML pages using section-type detection
(Overview, Features, Installation, Configuration, Screenshots, Usage,
Known Issues, FAQ, Changelog) with per-section customisable styles.
"""

from .converter import convert_md_to_html, __version__
from .utils import DEFAULT_SECTION_STYLES, SECTION_TYPE_KEYWORDS

__all__ = [
    "convert_md_to_html",
    "__version__",
    "DEFAULT_SECTION_STYLES",
    "SECTION_TYPE_KEYWORDS",
]
__author__ = "fasilwdr"
__description__ = "Section-type-aware Markdown to HTML converter for Odoo module pages"