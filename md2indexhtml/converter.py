# converter.py

import os
import sys
import argparse
import markdown
import re
from .utils import wrap_sections_bootstrap, handle_images

__version__ = "0.3.0"


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
                    processed_parts.append(wrap_sections_bootstrap(converted))

    return '\n'.join(processed_parts)


def convert_md_to_html(md_file_path=None, title="Documentation", output_path=None, template_style="modern"):
    """
    Convert a Markdown file to an HTML file with Bootstrap styling compatible with Odoo Apps Store.
    Preserves raw HTML sections while converting Markdown content, maintaining original order.
    Also handles image copying and path updates.

    :param md_file_path: Path to the markdown file
    :param title: Title of the HTML document
    :param output_path: Path where the output HTML file will be saved
    :param template_style: Style of the template ("modern", "simple", "odoo")
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

        # Select HTML template based on template_style
        if template_style == "simple":
            html_output = generate_simple_template(title, processed_content)
        elif template_style == "odoo":
            html_output = generate_odoo_template(title, processed_content)
        else:  # default to "modern"
            html_output = generate_modern_template(title, processed_content)

        # Write the output
        with open(output_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_output)

        print(f"Successfully converted {md_file_path} to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def generate_simple_template(title, content):
    """Generate a simple Bootstrap-based HTML template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{
            font-family: 'Inter', Arial, sans-serif;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            border-radius: 8px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        code {{
            background-color: #f3f3f3;
            color: #e74c3c;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding: 0.5rem 1rem;
            background-color: #f9f9f9;
        }}
        .card {{
            margin-bottom: 1rem;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .card-header {{
            background-color: #f8f9fa;
            border-bottom: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container my-5">
        {content}
    </div>
</body>
</html>"""


def generate_modern_template(title, content):
    """Generate a modern Bootstrap-based HTML template optimized for Odoo Apps Store"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{
            --primary-color: #003554;
            --secondary-color: #52A3AB;
            --text-color: #333;
            --light-bg: #f8f9fa;
            --card-bg: #fff;
        }}

        body {{
            font-family: 'Inter', Arial, sans-serif;
            color: var(--text-color);
            background-color: var(--light-bg);
            line-height: 1.6;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Montserrat', Arial, sans-serif;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }}

        h1 {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }}

        h2 {{
            font-size: 1.8rem;
            border-bottom: 2px solid #f1f1f1;
            padding-bottom: 0.5rem;
            margin-top: 2.5rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}

        code {{
            background-color: #f3f3f3;
            color: #e74c3c;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }}

        pre {{
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #eee;
            overflow-x: auto;
        }}

        blockquote {{
            border-left: 4px solid var(--primary-color);
            padding: 0.5rem 1rem;
            background-color: #f9f9f9;
            margin: 1.5rem 0;
        }}

        .card {{
            margin-bottom: 1.5rem;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: none;
        }}

        .card-header {{
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.25rem;
        }}

        .section-title {{
            text-align: center;
            margin: 3rem 0 2rem 0;
            position: relative;
        }}

        .section-title:after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 50px;
            height: 3px;
            background-color: var(--primary-color);
        }}

        .feature-item {{
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            height: 100%;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .feature-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .feature-icon {{
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}

        .alert {{
            border-radius: 8px;
            font-size: 0.95rem;
        }}

        /* Responsive adjustments */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem;
            }}

            h2 {{
                font-size: 1.5rem;
            }}
        }}
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
</head>
<body>
    <div class="container my-5 bg-white p-4 rounded shadow-sm">
        {content}
    </div>
    <script>
        // Add any custom JavaScript if needed
        document.addEventListener('DOMContentLoaded', function() {{
            // Initialize tooltips
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {{
                return new bootstrap.Tooltip(tooltipTriggerEl)
            }})
        }});
    </script>
</body>
</html>"""


def generate_odoo_template(title, content):
    """Generate an Odoo-style HTML template specifically designed for Odoo Apps Store with guaranteed responsive design"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
</head>
<body>
    <div id="wrap" class="oe_structure oe_empty">
        <section class="oe_container">
            <div class="oe_row oe_spaced">
                {content}
            </div>
        </section>
    </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to styled HTML for Odoo modules'
    )
    parser.add_argument('file', nargs='?', help='Path to the markdown file (optional)')
    parser.add_argument('--version', action='version',
                        version=f'md2indexhtml {__version__}')
    parser.add_argument('--title', help='Specify a custom title for the HTML document', default="Documentation")
    parser.add_argument('--output', '-o', help='Specify a custom output path for the HTML file')
    parser.add_argument('--template', '-t',
                        choices=['modern', 'simple', 'odoo'],
                        default='odoo',
                        help='Template style to use (modern, simple, or odoo)')

    args = parser.parse_args()

    try:
        convert_md_to_html(args.file, args.title, args.output, args.template)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()