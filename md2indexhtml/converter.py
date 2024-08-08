# md2indexhtml/converter.py

import argparse
import os
import shutil  # Import shutil for file operations
import markdown
from .utils import load_template

def convert_md_to_html(md_file_path, output_dir, template_path=None, custom_css_path=None):
    """
    Convert a Markdown file to an HTML file using a specified template and optional custom CSS.

    :param md_file_path: Path to the Markdown file.
    :param output_dir: Directory to save the output HTML file.
    :param template_path: Path to the HTML template (optional).
    :param custom_css_path: Path to a custom CSS file (optional).
    """
    # Read the Markdown file
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Convert Markdown to HTML with the table extension
    html_content = markdown.markdown(md_content, extensions=['tables'])

    # Load the HTML template
    template = load_template(template_path or 'index_template')

    # Add custom CSS link if provided
    custom_css_link = f'<link rel="stylesheet" href="{os.path.basename(custom_css_path)}">' if custom_css_path else ''

    # Combine the template and the HTML content
    html_output = template.replace('{{ content }}', html_content).replace('{{ custom_css }}', custom_css_link)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the output to an HTML file
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_output)

    # Copy the custom CSS file to the output directory if provided
    if custom_css_path:
        try:
            shutil.copy(custom_css_path, output_dir)
            print(f"Copied {custom_css_path} to {output_dir}")
        except Exception as e:
            print(f"Failed to copy CSS file: {e}")

    print(f"Converted {md_file_path} to {output_path}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert a Markdown file to an HTML file.')
    parser.add_argument('md_file_path', type=str, help='Path to the Markdown file.')
    parser.add_argument('output_dir', type=str, help='Directory to save the output HTML file.')
    parser.add_argument('--template', type=str, help='Path to the HTML template (optional).')
    parser.add_argument('--css', type=str, help='Path to a custom CSS file (optional).')

    # Parse arguments
    args = parser.parse_args()

    # Call the conversion function with the parsed arguments
    convert_md_to_html(args.md_file_path, args.output_dir, args.template, args.css)

if __name__ == '__main__':
    main()
