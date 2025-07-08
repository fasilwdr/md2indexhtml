# converter.py - Updated with default Odoo styling only

import os
import sys
import argparse
import markdown
import re
from .utils import wrap_sections_odoo, handle_images, DEFAULT_STYLE_CONFIG
from typing import Optional, Dict

__version__ = "0.5.0"


def process_content_blocks(content, md_file_path, output_dir, style_config=None):
    """
    Process content maintaining the original order of HTML and markdown blocks

    :param content: Mixed content string
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
    :param style_config: Dictionary configuration for styling elements
    :return: Processed HTML content with preserved order
    """
    # Split content by horizontal rules (---) to create sections
    sections = re.split(r'\n\s*---+\s*\n', content)
    processed_sections = []

    for section in sections:
        if section.strip():
            # Extract HTML sections (content between <section> tags)
            html_parts = re.split(r'(<section.*?</section>)', section, flags=re.DOTALL)

            for part in html_parts:
                if part.strip():
                    if part.strip().startswith('<section'):
                        # Process images in HTML but preserve the structure
                        processed_html = handle_images(part, md_file_path, output_dir)
                        processed_sections.append(processed_html)
                    else:
                        # Process regular markdown content
                        processed_part = handle_images(part, md_file_path, output_dir)
                        # Convert markdown to HTML
                        converted = markdown.markdown(
                            processed_part,
                            extensions=[
                                'tables',
                                'fenced_code',
                                'codehilite',
                                'nl2br',
                                'sane_lists',
                                'attr_list'
                            ]
                        )
                        if converted.strip():
                            processed_sections.append(converted)

    return '\n'.join(processed_sections)


def convert_md_to_html(
        md_file_path: Optional[str] = None,
        title: str = "Documentation",
        output_path: Optional[str] = None,
        style_config: Optional[Dict[str, Dict[str, str]]] = None
):
    """
    Convert a Markdown file to an HTML file using Odoo frontend styling

    :param md_file_path: Path to the markdown file
    :param title: Title of the HTML document
    :param output_path: Path where the output HTML file will be saved
    :param style_config: Dictionary configuration for styling elements
                        Format: {"element": {"attribute": "value"}}
                        Example: {"p": {"class": "mb16"}, "table": {"class": "table table-bordered"}}
                        If None, uses DEFAULT_STYLE_CONFIG with comprehensive Odoo classes
    :return: Path to the generated HTML file
    """
    try:
        # Handle file path logic
        if md_file_path:
            md_file_path = os.path.abspath(md_file_path)
        else:
            md_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.md')]
            if md_files:
                md_file_path = os.path.join(os.getcwd(), md_files[0])
            else:
                raise FileNotFoundError("No markdown file found in current directory")

        if not os.path.exists(md_file_path):
            raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

        # Handle output path logic
        if output_path:
            output_path = os.path.abspath(output_path)
            output_dir = os.path.dirname(output_path)
        else:
            output_dir = os.path.join(os.path.dirname(md_file_path), 'static', 'description')
            output_path = os.path.join(output_dir, 'index.html')

        os.makedirs(output_dir, exist_ok=True)

        # Use default Odoo styling if no custom config provided
        if style_config is None:
            style_config = DEFAULT_STYLE_CONFIG

        # Read the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()

        # Process content blocks maintaining order and handle images
        processed_content = process_content_blocks(content, md_file_path, output_dir, style_config)

        # Wrap content in Odoo-styled sections
        html_output = wrap_sections_odoo(processed_content, title)

        # Write the output
        with open(output_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_output)

        print(f"Successfully converted {md_file_path} to {output_path}")
        if style_config and style_config != DEFAULT_STYLE_CONFIG:
            print(f"Applied custom styling configuration")
        else:
            print(f"Applied default Odoo styling configuration")
        return output_path

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def create_style_config_from_file(config_file_path: str) -> Dict[str, Dict[str, str]]:
    """
    Load style configuration from a JSON file

    :param config_file_path: Path to JSON configuration file
    :return: Style configuration dictionary
    """
    import json

    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Validate the configuration format
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        for element, attributes in config.items():
            if not isinstance(attributes, dict):
                raise ValueError(f"Attributes for element '{element}' must be a dictionary")

        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error loading configuration file: {str(e)}")


def show_default_config():
    """
    Display the default Odoo styling configuration
    """
    print("Default Odoo Styling Configuration:")
    print("=" * 50)

    # Group elements by category for better display
    categories = {
        "Typography": ["h1", "h2", "h3", "h4", "h5", "h6", "p", "strong", "em", "small", "mark"],
        "Lists": ["ul", "ol", "li", "dl", "dt", "dd"],
        "Tables": ["table", "thead", "tbody", "tr", "th", "td"],
        "Code": ["pre", "code"],
        "Media": ["img", "figure", "figcaption"],
        "Layout": ["div", "section", "article", "main", "aside", "header", "footer"],
        "Forms": ["form", "fieldset", "legend", "label", "input", "textarea", "select", "button"],
        "Other": ["blockquote", "a", "hr", "span", "address", "cite", "abbr", "time"]
    }

    for category, elements in categories.items():
        print(f"\n{category}:")
        print("-" * len(category))
        for element in elements:
            if element in DEFAULT_STYLE_CONFIG:
                attrs = DEFAULT_STYLE_CONFIG[element]
                print(f"  {element}: {attrs}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to styled HTML for Odoo modules with comprehensive frontend classes'
    )
    parser.add_argument('file', nargs='?', help='Path to the markdown file (optional)')
    parser.add_argument('--version', action='version',
                        version=f'md2indexhtml {__version__}')
    parser.add_argument('--title', help='Specify a custom title for the HTML document', default="Documentation")
    parser.add_argument('--output', '-o', help='Specify a custom output path for the HTML file')
    parser.add_argument('--style-config', help='Path to JSON file containing custom style configuration')
    parser.add_argument('--show-config', action='store_true',
                        help='Display the default Odoo styling configuration and exit')

    args = parser.parse_args()

    # Show default configuration if requested
    if args.show_config:
        show_default_config()
        return

    try:
        style_config = None

        # Load custom style configuration if provided
        if args.style_config:
            style_config = create_style_config_from_file(args.style_config)
            print(f"Loaded custom style configuration from {args.style_config}")

        convert_md_to_html(
            md_file_path=args.file,
            title=args.title,
            output_path=args.output,
            style_config=style_config
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()