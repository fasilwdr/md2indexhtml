# utils.py - Updated with Comprehensive Odoo Frontend Classes

import re
import os
import shutil
from typing import Dict, Optional

# Comprehensive Odoo styling configuration using classes from web.assets_frontend.min.css
DEFAULT_STYLE_CONFIG: Dict[str, Dict[str, str]] = {
    # Typography - Headers
    "h1": {"class": "display-4 text-center mb32 text-primary font-weight-bold"},
    "h2": {"class": "h2 mb24 text-secondary font-weight-bold border-bottom pb-2"},
    "h3": {"class": "h3 mb16 text-primary font-weight-semibold"},
    "h4": {"class": "h4 mb12 text-dark font-weight-medium"},
    "h5": {"class": "h5 mb8 text-muted"},
    "h6": {"class": "h6 mb8 text-muted"},

    # Typography - Text elements
    "p": {"class": "mb16 text-justify"},
    "strong": {"class": "font-weight-bold text-dark"},
    "em": {"class": "font-italic text-muted"},
    "small": {"class": "small text-muted"},
    "mark": {"class": "bg-warning text-dark"},

    # Lists
    "ul": {"class": "mb16 pl-4"},
    "ol": {"class": "mb16 pl-4"},
    "li": {"class": "mb8"},
    "dl": {"class": "mb16"},
    "dt": {"class": "font-weight-bold mb4"},
    "dd": {"class": "mb8 ml-4"},

    # Tables
    "table": {"class": "table table-striped table-hover table-bordered mb16 w-100"},
    "thead": {"class": "thead-light"},
    "tbody": {"class": ""},
    "tr": {"class": ""},
    "th": {"class": "text-center font-weight-bold bg-light"},
    "td": {"class": "text-left align-middle"},

    # Code blocks
    "pre": {"class": "bg-light border rounded p-3 mb16 overflow-auto"},
    "code": {"class": "bg-light text-danger px-2 py-1 rounded border"},

    # Quote blocks
    "blockquote": {"class": "blockquote mb16 border-left border-primary pl-3 bg-light p-3 rounded"},

    # Images and media
    "img": {"class": "img-fluid rounded shadow-sm mb16 d-block mx-auto"},
    "figure": {"class": "figure mb16 text-center"},
    "figcaption": {"class": "figure-caption text-muted mt-2"},

    # Links
    "a": {"class": "text-primary text-decoration-none"},

    # Divisions and containers
    "div": {"class": "mb16"},
    "section": {"class": "py-4"},
    "article": {"class": "mb32"},
    "main": {"class": "container-fluid"},
    "aside": {"class": "bg-light p-3 rounded mb16"},
    "header": {"class": "mb24 pb-3 border-bottom"},
    "footer": {"class": "mt24 pt-3 border-top text-muted"},

    # Form elements
    "form": {"class": "mb16"},
    "fieldset": {"class": "mb16 p-3 border rounded"},
    "legend": {"class": "font-weight-bold mb16"},
    "label": {"class": "font-weight-medium mb-2"},
    "input": {"class": "form-control mb-3"},
    "textarea": {"class": "form-control mb-3"},
    "select": {"class": "form-control mb-3"},
    "button": {"class": "btn btn-primary"},

    # Navigation
    "nav": {"class": "mb16"},
    "ul.nav": {"class": "nav nav-pills mb16"},
    "li.nav-item": {"class": "nav-item"},
    "a.nav-link": {"class": "nav-link"},

    # Cards and panels
    "div.card": {"class": "card mb16 shadow-sm"},
    "div.card-header": {"class": "card-header bg-primary text-white font-weight-bold"},
    "div.card-body": {"class": "card-body"},
    "div.card-footer": {"class": "card-footer bg-light text-muted"},

    # Alerts and badges
    "div.alert": {"class": "alert alert-info mb16"},
    "span.badge": {"class": "badge badge-secondary"},

    # Media objects
    "div.media": {"class": "media mb16"},
    "div.media-object": {"class": "media-object"},
    "div.media-body": {"class": "media-body"},

    # Grid system helpers
    "div.container": {"class": "container"},
    "div.row": {"class": "row"},
    "div.col": {"class": "col"},

    # Utility classes for common elements
    "hr": {"class": "my-4 border-top"},
    "br": {"class": ""},
    "span": {"class": ""},
    "address": {"class": "mb16 font-italic"},
    "cite": {"class": "font-italic text-muted"},
    "abbr": {"class": "text-decoration-underline"},
    "time": {"class": "text-muted"},

    # Definition lists
    "dl.row": {"class": "row mb16"},
    "dt.col-sm-3": {"class": "col-sm-3 font-weight-bold"},
    "dd.col-sm-9": {"class": "col-sm-9"},

    # Progress and meters
    "progress": {"class": "progress mb16"},
    "meter": {"class": "mb16"},

    # Details and summary
    "details": {"class": "mb16 border rounded p-3"},
    "summary": {"class": "font-weight-bold cursor-pointer"},

    # Interactive elements
    "kbd": {"class": "kbd"},
    "samp": {"class": "text-monospace bg-light px-1"},
    "var": {"class": "font-italic text-info"},

    # Semantic HTML5 elements
    "main": {"class": "main-content"},
    "section.hero": {"class": "py-5 bg-primary text-white text-center"},
    "section.features": {"class": "py-4"},
    "section.testimonials": {"class": "py-4 bg-light"},
    "section.cta": {"class": "py-5 bg-secondary text-white text-center"},
}


def handle_images(content: str, md_file_path: str, output_dir: str) -> str:
    """
    Process image paths in content and copy images to output directory
    All local images are copied to images/ directory in output_dir
    Only filenames are kept, discarding original directory structure

    :param content: HTML content
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
    :return: Updated content with new image paths
    """

    def is_local_path(path: str) -> bool:
        """Check if the path is a local file path"""
        return not (path.startswith(('http://', 'https://', 'data:', '/web/', 'www.')) or
                    path.startswith('data:image/'))

    def process_image_path(img_path: str) -> str:
        """Process and copy local image if needed"""
        img_path = img_path.strip("'\" ")

        # If the path starts with 'static/description/', just remove the prefix and return
        if img_path.startswith('static/description/'):
            return img_path[18:]

        # Skip non-local paths and base64 images
        if not is_local_path(img_path):
            return img_path

        try:
            # Get absolute paths
            md_dir = os.path.dirname(os.path.abspath(md_file_path))
            abs_img_path = os.path.normpath(os.path.join(md_dir, img_path))

            # Skip if image doesn't exist
            if not os.path.isfile(abs_img_path):
                print(f"Warning: Image not found at {abs_img_path}")
                return img_path

            # Create images directory in output path
            images_dir = os.path.join(output_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)

            # Get just the filename from the path
            filename = os.path.basename(img_path)

            # Copy the image to images directory
            target_path = os.path.join(images_dir, filename)
            shutil.copy2(abs_img_path, target_path)

            return f'images/{filename}'

        except Exception as e:
            print(f"Warning: Failed to process image {img_path}: {str(e)}")
            return img_path

    # Handle Markdown image syntax
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
                     lambda
                         m: f'<img alt="{m.group(1)}" src="{process_image_path(m.group(2))}" class="img img-fluid"/>',
                     content)

    # Handle HTML image syntax
    content = re.sub(r'src=(["\'])(.*?)\1',
                     lambda m: f'src="{process_image_path(m.group(2))}"',
                     content)

    return content


def wrap_sections_odoo(content: str, title: str) -> str:
    """
    Wrap HTML content in Odoo-styled sections based on headings

    :param content: HTML content as string
    :param title: Title of the document
    :return: Wrapped HTML content with Odoo styling
    """
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Generated by md2indexhtml">
    <title>{title}</title>
    <style>
        /* Ensure Odoo-specific styles are applied */
        .oe_structure {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #212529;
        }}
        .pt32 {{ padding-top: 2rem !important; }}
        .pb32 {{ padding-bottom: 2rem !important; }}
        .mb32 {{ margin-bottom: 2rem !important; }}
        .mb24 {{ margin-bottom: 1.5rem !important; }}
        .mb16 {{ margin-bottom: 1rem !important; }}
        .mb12 {{ margin-bottom: 0.75rem !important; }}
        .mb8 {{ margin-bottom: 0.5rem !important; }}
        .mb4 {{ margin-bottom: 0.25rem !important; }}
        .mt24 {{ margin-top: 1.5rem !important; }}
        .pl-4 {{ padding-left: 1.5rem !important; }}
        .ml-4 {{ margin-left: 1.5rem !important; }}
        .font-weight-bold {{ font-weight: 700 !important; }}
        .font-weight-semibold {{ font-weight: 600 !important; }}
        .font-weight-medium {{ font-weight: 500 !important; }}
        .text-justify {{ text-align: justify !important; }}
    </style>
</head>
<body>
    <div class="oe_structure">
        {process_headings(content)}
    </div>
</body>
</html>'''

    return html_template


def process_headings(content: str) -> str:
    """
    Process content and organize it based on heading levels

    :param content: HTML content
    :return: Processed content with Odoo section structure
    """
    # First, extract and preserve any existing <section> tags
    sections = []
    raw_html_sections = re.finditer(r'(<section.*?</section>)', content, flags=re.DOTALL)
    last_end = 0

    for match in raw_html_sections:
        # Add any content before this section
        if match.start() > last_end:
            sections.append(process_markdown_section(content[last_end:match.start()]))

        # Add the raw HTML section as is
        sections.append(match.group(1))
        last_end = match.end()

    # Add any remaining content
    if last_end < len(content):
        sections.append(process_markdown_section(content[last_end:]))

    return '\n'.join(filter(None, sections))


def process_markdown_section(content: str) -> str:
    """
    Process markdown content into Odoo-styled sections

    :param content: HTML content from markdown conversion
    :return: Processed content with Odoo section structure
    """
    if not content.strip():
        return ''

    # Split content by h1 tags
    h1_parts = re.split(r'(<h1.*?</h1>)', content, flags=re.DOTALL)
    processed_content = []

    for i in range(1, len(h1_parts), 2):
        if i < len(h1_parts):
            h1_content = h1_parts[i]
            following_content = h1_parts[i + 1] if i + 1 < len(h1_parts) else ''

            # Extract h1 text
            h1_text = re.search(r'>([^<]+)</h1>', h1_content)
            h1_text = h1_text.group(1) if h1_text else ''

            # Start new section for h1
            section = f'''
                <section class="pt32 pb32">
                    <div class="container">
                        <h1 class="text-center mb32">{h1_text}</h1>
            '''

            # Process content immediately after h1 but before any h2
            h2_split = re.split(r'(<h2.*?</h2>)', following_content, flags=re.DOTALL)
            if h2_split[0].strip():
                section += f'''
                    <div class="mb32">
                        {process_block_content(h2_split[0])}
                    </div>
                '''

            # If there are h2 headings, process them
            if len(h2_split) > 1:
                # Start row for h2 sections
                section += '<div class="row d-flex align-items-stretch">'

                # Process all h2 sections
                for j in range(1, len(h2_split), 2):
                    if j < len(h2_split):
                        h2_content = h2_split[j]
                        h2_following = h2_split[j + 1] if j + 1 < len(h2_split) else ''

                        # Extract h2 text
                        h2_text = re.search(r'>([^<]+)</h2>', h2_content)
                        h2_text = h2_text.group(1) if h2_text else ''

                        # Determine column width based on number of h2 sections
                        col_class = "col-lg-12" if len(h2_split) == 3 else "col-lg-6"

                        section += f'''
                            <div class="{col_class} d-flex">
                                <div class="card w-100 mb16">
                                    <div class="card-header">
                                        <h2 class="text-center mb0">{h2_text}</h2>
                                    </div>
                                    <div class="card-body">
                                        {process_block_content(h2_following)}
                                    </div>
                                </div>
                            </div>
                        '''

                section += '</div>'  # Close row

            section += '''
                    </div>
                </section>
            '''

            processed_content.append(section)

    return '\n'.join(processed_content)


def apply_element_styling(content: str, element: str, attributes: Dict[str, str]) -> str:
    """
    Apply multiple attributes to HTML elements using regex

    :param content: HTML content
    :param element: HTML element name (e.g., 'p', 'div', 'table')
    :param attributes: Dictionary of attributes to apply {'class': 'mb16', 'id': 'main'}
    :return: Modified content with applied attributes
    """

    def add_attributes(match):
        tag = match.group(0)

        # Build attributes string
        attr_strings = []
        for attr_name, attr_value in attributes.items():
            # Check if attribute already exists in the tag
            existing_attr_pattern = rf'{attr_name}=(["\'])([^"\']*?)\1'
            existing_match = re.search(existing_attr_pattern, tag)

            if existing_match:
                # Attribute exists, handle based on type
                if attr_name == "class":
                    # For class, append new classes to existing ones
                    quote = existing_match.group(1)
                    existing_value = existing_match.group(2)
                    new_value = f"{existing_value} {attr_value}".strip()
                    tag = re.sub(existing_attr_pattern, f'{attr_name}={quote}{new_value}{quote}', tag)
                else:
                    # For other attributes, replace the value
                    quote = existing_match.group(1)
                    tag = re.sub(existing_attr_pattern, f'{attr_name}={quote}{attr_value}{quote}', tag)
            else:
                # Attribute doesn't exist, add it
                attr_strings.append(f'{attr_name}="{attr_value}"')

        # Add new attributes if any
        if attr_strings:
            new_attrs = ' ' + ' '.join(attr_strings)
            if tag.endswith('>'):
                tag = tag[:-1] + new_attrs + '>'
            else:
                tag = tag + new_attrs

        return tag

    # Apply to opening tags only
    pattern = f'<{element}(?:\\s[^>]*)?>'
    return re.sub(pattern, add_attributes, content)


def process_block_content(
        content: str,
        style_config: Optional[Dict[str, Dict[str, str]]] = None
) -> str:
    """
    Process block content and apply configurable styling using dictionary format

    :param content: HTML content block
    :param style_config: Dictionary configuration for styling elements
                        Format: {
                            "element_name": {
                                "attribute_name": "attribute_value",
                                "class": "css-classes",
                                "id": "element-id"
                            }
                        }
                        Example: {
                            "p": {"class": "mb16"},
                            "table": {"class": "table table-bordered mb16", "id": "main-table"}
                        }
    :return: Processed content with applied styles
    """
    # Remove extra whitespace
    content = content.strip()

    # Use default configuration if none provided
    if style_config is None:
        style_config = DEFAULT_STYLE_CONFIG

    # Validate configuration format
    if not isinstance(style_config, dict):
        raise ValueError("style_config must be a dictionary")

    # Apply styling for each element in configuration
    for element, attributes in style_config.items():
        if not isinstance(attributes, dict):
            print(f"Warning: Invalid attributes for element '{element}'. Expected dict, got {type(attributes)}")
            continue

        if not attributes:  # Skip empty attribute dictionaries
            continue

        try:
            content = apply_element_styling(content, element, attributes)
        except Exception as e:
            print(f"Warning: Failed to apply styling to element '{element}': {str(e)}")

    return content