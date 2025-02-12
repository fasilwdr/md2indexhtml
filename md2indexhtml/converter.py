import os
import sys
import argparse
import markdown
from markdown.extensions.toc import TocExtension
from .utils import extract_title_and_headers, get_default_styles, apply_styles_to_html

__version__ = "0.1.6"


def convert_md_to_html(md_file_path=None, title="Documentation", output_path=None):
    """
    Convert a Markdown file to an HTML file with inline styles.

    :param md_file_path: Path to the Markdown file (optional).
                        If not provided, uses the first .md file in current directory
    :param title: Title for the HTML document (optional).
    :param output_path: Custom output path for the HTML file (optional).
                       If not provided, uses 'static/description/index.html'
    """
    try:
        # If md_file_path is provided as an argument
        if md_file_path:
            # Convert to absolute path
            md_file_path = os.path.abspath(md_file_path)
        else:
            # Look for any .md file in current directory
            md_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.md')]
            if md_files:
                md_file_path = os.path.join(os.getcwd(), md_files[0])
            else:
                raise FileNotFoundError("No markdown file found in current directory")

        # Ensure the markdown file exists
        if not os.path.exists(md_file_path):
            raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

        # Determine output path
        if output_path:
            # Use the provided output path
            output_path = os.path.abspath(output_path)
            output_dir = os.path.dirname(output_path)
        else:
            # Use default path in static/description/
            output_dir = os.path.join(os.path.dirname(md_file_path), 'static', 'description')
            output_path = os.path.join(output_dir, 'index.html')

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Read the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Extract title and headers
        md_title, toc_html = extract_title_and_headers(md_content)

        # Use provided title if given, otherwise use extracted title
        page_title = title or md_title

        # Convert Markdown to HTML with extensions
        html_content = markdown.markdown(
            md_content,
            extensions=[
                'tables',
                'fenced_code',
                TocExtension(anchorlink=True),
                'codehilite',
                'nl2br',
                'sane_lists',
                'attr_list'
            ]
        )

        # Get default styles
        styles = get_default_styles()

        # Create the HTML output with inline styles
        html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
</head>
<body>
<div class="md-container" style="{'; '.join([f'{k}: {v}' for k, v in styles['md-container'].items()])}" data-title="{page_title}">
    <div class="markdown-body" style="{'; '.join([f'{k}: {v}' for k, v in styles['markdown-body'].items()])}">
        {html_content[:html_content.find('</h1>') + 5] if '</h1>' in html_content else html_content}
        <div class="toc-container" style="{'; '.join([f'{k}: {v}' for k, v in styles['toc-container'].items()])}">
            <h2 style="{'; '.join([f'{k}: {v}' for k, v in styles['toc-h2'].items()])}">Table of Contents</h2>
            {toc_html}
        </div>
        {html_content[html_content.find('</h1>') + 5:] if '</h1>' in html_content else ''}
    </div>
</div>
</body>
</html>"""

        # Apply styles to the HTML content
        html_output = apply_styles_to_html(html_output, styles)

        # Write the output to an HTML file
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
    parser.add_argument('--title', help='Specify a custom title for the HTML document')
    parser.add_argument('--output', '-o', help='Specify a custom output path for the HTML file')

    args = parser.parse_args()

    try:
        convert_md_to_html(args.file, args.title, args.output)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()