import os
import sys
import markdown
from markdown.extensions.toc import TocExtension
from .utils import extract_title_and_headers, get_default_styles, apply_styles_to_html

__version__ = "0.1.5"


def convert_md_to_html(md_file_path=None, title="Documentation"):
    """
    Convert a Markdown file to an HTML file with inline styles.

    :param md_file_path: Path to the Markdown file (optional).
                        If not provided, uses 'static/description/index.html'
    :param title: Title for the HTML document (optional).
    """
    try:
        # If md_file_path is provided as an argument
        if md_file_path:
            # Convert to absolute path
            md_file_path = os.path.abspath(md_file_path)
            # Create output path in static/description/
            filename = os.path.basename(md_file_path)
            base_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(os.path.dirname(md_file_path), 'static', 'description')
            output_path = os.path.join(output_dir, 'index.html')
        else:
            # Use default path
            output_dir = os.path.join(os.getcwd(), 'static', 'description')
            output_path = os.path.join(output_dir, 'index.html')
            # Look for any .md file in current directory
            md_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.md')]
            if md_files:
                md_file_path = os.path.join(os.getcwd(), md_files[0])
            else:
                raise FileNotFoundError("No markdown file found in current directory")

        # Ensure the markdown file exists
        if not os.path.exists(md_file_path):
            raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

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
        html_output = f"""
<!DOCTYPE html>
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
</html>
"""

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
    # Get command line arguments
    args = sys.argv[1:]

    if args:
        # If argument provided, use it as markdown file path
        convert_md_to_html(args[0])
    else:
        # If no argument, try to convert markdown file in current directory
        convert_md_to_html()


if __name__ == '__main__':
    main()