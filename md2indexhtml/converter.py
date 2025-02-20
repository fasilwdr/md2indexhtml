# converter.py

import os
import sys
import argparse
import markdown
import re
from .utils import wrap_sections, handle_images

__version__ = "0.2.1"


def process_content_blocks(content, md_file_path, output_dir):
    """
    Process content maintaining the original order of HTML and Markdown blocks

    :param content: Mixed content string
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
    :return: Processed HTML content with preserved order
    """
    # Pattern to match complete HTML section blocks
    pattern = r'(<section[\s\S]*?</section>)'

    # Split content and track what we've processed
    parts = re.split(f'({pattern})', content, flags=re.DOTALL)
    processed_parts = []
    seen_sections = set()

    for part in parts:
        if part.strip():  # Skip empty parts
            # Check if this is a section block
            is_section = bool(re.match(pattern, part.strip()))

            if is_section:
                # Process images in HTML sections
                processed_part = handle_images(part, md_file_path, output_dir)
                # Hash the content to check for duplicates
                section_hash = hash(processed_part.strip())
                if section_hash not in seen_sections:
                    seen_sections.add(section_hash)
                    processed_parts.append(processed_part)
            else:
                # Convert markdown content
                converted = markdown.markdown(
                    part,
                    extensions=[
                        'tables',
                        'fenced_code',
                        'codehilite',
                        'nl2br',
                        'sane_lists',
                        'attr_list'
                    ]
                )
                if converted.strip():  # Only wrap if there's content
                    # Process images in converted markdown
                    converted = handle_images(converted, md_file_path, output_dir)
                    processed_parts.append(wrap_sections(converted))

    return '\n'.join(processed_parts)


def convert_md_to_html(md_file_path=None, title="Documentation", output_path=None):
    """
    Convert a Markdown file to an HTML file with inline styles and section-based structure.
    Preserves raw HTML sections while converting Markdown content, maintaining original order.
    Also handles image copying and path updates.
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

        # Create the final HTML output with inline styles
        html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
    <title>{title}</title>
</head>
<body style="font-family: Inter, Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f6fa;">
    <div style="padding: 20px; background: #f5f6fa">
        <div style="font-family: Inter, Arial, sans-serif; line-height: 1.6; background: #ffffff; max-width: 1200px; margin: 0 auto">
            {processed_content}
        </div>
    </div>
</body>
</html>"""

        # Write the output
        with open(output_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_output)

        print(f"Successfully converted {md_file_path} to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to styled HTML for Odoo modules'
    )
    parser.add_argument('file', nargs='?', help='Path to the markdown file (optional)')
    parser.add_argument('--version', action='version',
                       version=f'md2indexhtml {__version__}')
    parser.add_argument('--title', help='Specify a custom title for the HTML document', default="Documentation")
    parser.add_argument('--output', '-o', help='Specify a custom output path for the HTML file')

    args = parser.parse_args()

    try:
        convert_md_to_html(args.file, args.title, args.output)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()