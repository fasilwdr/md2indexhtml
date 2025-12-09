# converter.py - Updated with default Odoo styling only

import os
import sys
import argparse
import markdown
import re
from .utils import wrap_sections_odoo, handle_images, DEFAULT_STYLE_CONFIG
from typing import Optional, Dict

__version__ = "0.6.0"


def process_content_blocks(content, md_file_path, output_dir):
    """
    Process content maintaining the original order of HTML and markdown blocks

    :param content: Mixed content string
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
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
        stylesheets: Optional[list] = None,
        scripts: Optional[list] = None
):
    """
    Convert a Markdown file to an HTML file using Odoo frontend styling

    :param md_file_path: Path to the markdown file
    :param title: Title of the HTML document
    :param output_path: Path where the output HTML file will be saved
    :param stylesheets: List of stylesheet URLs/paths to include
    :param scripts: List of script URLs/paths to include
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

        # Read the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            content = md_file.read()

        # Process content blocks maintaining order and handle images
        processed_content = process_content_blocks(content, md_file_path, output_dir)

        # Wrap content in Odoo-styled sections
        html_output = wrap_sections_odoo(processed_content, title, stylesheets, scripts)

        # Write the output
        with open(output_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_output)

        print(f"Successfully converted {md_file_path} to {output_path}")
        print(f"Applied default Odoo styling configuration")
        return output_path

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to styled HTML for Odoo modules with comprehensive frontend classes'
    )
    parser.add_argument('file', nargs='?', help='Path to the markdown file (optional)')
    parser.add_argument('--version', action='version',
                        version=f'md2indexhtml {__version__}')
    parser.add_argument('--title', help='Specify a custom title for the HTML document', default="Documentation")
    parser.add_argument('--output', '-o', help='Specify a custom output path for the HTML file')
    
    # New arguments
    parser.add_argument('--stylesheet', help='Comma-separated list of stylesheets (URL or path) to include')
    parser.add_argument('--script', help='Comma-separated list of scripts (URL or path) to include')

    args = parser.parse_args()

    try:
        # Parse comma-separated lists
        stylesheets = args.stylesheet.split(',') if args.stylesheet else None
        scripts = args.script.split(',') if args.script else None

        if stylesheets:
            stylesheets = [s.strip() for s in stylesheets if s.strip()]
        if scripts:
            scripts = [s.strip() for s in scripts if s.strip()]

        convert_md_to_html(
            md_file_path=args.file,
            title=args.title,
            output_path=args.output,
            stylesheets=stylesheets,
            scripts=scripts
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()