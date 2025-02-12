import re


def extract_title_and_headers(md_content):
    """
    Extract the title (first header) and generate a table of contents from headers.

    :param md_content: Markdown content as a string.
    :return: Tuple containing the title and the HTML for the table of contents.
    """
    lines = md_content.split('\n')
    title = ""
    toc_html = "<ul>"

    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            toc_html += f'<li class="level-1"><a href="#{slugify(title)}">{title}</a></li>'
        elif line.startswith("## "):
            header = line.lstrip("## ").strip()
            toc_html += f'<li class="level-2"><a href="#{slugify(header)}">{header}</a></li>'
        elif line.startswith("### "):
            sub_header = line.lstrip("### ").strip()
            toc_html += f'<li class="level-3"><a href="#{slugify(sub_header)}">{sub_header}</a></li>'

    toc_html += "</ul>"

    return title, toc_html


def slugify(value, separator='-'):
    """
    Convert a string into a slug for use in URLs and IDs.

    :param value: String to be converted to a slug.
    :param separator: Separator to use for spaces.
    :return: Slugified string.
    """
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', separator, value)


def get_default_styles():
    """Return a dictionary of default styles for different HTML elements"""
    return {
        'markdown-body': {
            'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            'line-height': '1.6',
            'padding': '20px',
            'background': '#ffffff',
            'border-radius': '8px',
            'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
            'max-width': '1200px',
            'margin': '0 auto'
        },
        'h1': {
            'color': '#2c3e50',
            'border-bottom': '2px solid #3498db',
            'padding-bottom': '10px',
            'margin-bottom': '20px'
        },
        'h2': {
            'color': '#34495e',
            'border-bottom': '1px solid #bdc3c7',
            'padding-bottom': '5px'
        },
        'h3,h4,h5,h6': {
            'color': '#16a085'
        },
        'code': {
            'background': '#f8f9fa',
            'color': '#e74c3c',
            'padding': '2px 5px',
            'border-radius': '3px',
            'font-family': '"Monaco", "Menlo", "Ubuntu Mono", "Consolas", monospace'
        },
        'pre': {
            'background': '#2c3e50',
            'color': '#ecf0f1',
            'padding': '15px',
            'border-radius': '5px',
            'overflow-x': 'auto'
        },
        'pre code': {
            'background': 'transparent',
            'color': '#ecf0f1',
            'padding': '0'
        },
        'blockquote': {
            'border-left': '4px solid #3498db',
            'padding': '10px 15px',
            'margin': '10px 0',
            'background': '#f7f9fc',
            'color': '#34495e'
        },
        'table': {
            'border-collapse': 'collapse',
            'width': '100%',
            'margin': '15px 0'
        },
        'th': {
            'background': '#3498db',
            'color': 'white',
            'padding': '10px',
            'border': '1px solid #2980b9'
        },
        'td': {
            'padding': '8px',
            'border': '1px solid #bdc3c7'
        },
        'tr:nth-child(even)': {
            'background': '#f7f9fc'
        },
        'a': {
            'color': '#3498db',
            'text-decoration': 'none',
            'border-bottom': '1px solid transparent',
            'transition': 'border-color 0.2s'
        },
        'a:hover': {
            'border-bottom-color': '#3498db'
        },
        'ul,ol': {
            'padding-left': '20px'
        },
        'li': {
            'margin': '5px 0'
        },
        'hr': {
            'border': 'none',
            'border-top': '2px solid #ecf0f1',
            'margin': '20px 0'
        },
        'img': {
            'max-width': '100%',
            'border-radius': '5px',
            'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
        },
        'toc-container': {
            'background': '#f8f9fa',
            'border-radius': '8px',
            'padding': '20px',
            'margin': '20px 0',
            'border': '1px solid #e9ecef'
        },
        'toc-h2': {
            'color': '#2c3e50',
            'margin-top': '0',
            'font-size': '1.5em'
        },
        'toc-ul': {
            'list-style': 'none',
            'padding': '0',
            'margin': '0'
        },
        'toc-li': {
            'margin': '8px 0'
        },
        'level-1': {
            'margin-left': '0'
        },
        'level-2': {
            'margin-left': '20px'
        },
        'level-3': {
            'margin-left': '40px'
        },
        'toc-a': {
            'color': '#34495e',
            'text-decoration': 'none',
            'display': 'block',
            'padding': '5px 10px',
            'border-radius': '4px',
            'transition': 'all 0.2s'
        },
        'md-container': {
            'padding': '20px',
            'background': '#f5f6fa'
        }
    }


def apply_styles_to_html(html_content, styles):
    """
    Apply inline styles to HTML elements

    :param html_content: HTML content as string
    :param styles: Dictionary of styles to apply
    :return: HTML content with applied styles
    """
    for element, style_dict in styles.items():
        style_str = '; '.join([f'{k}: {v}' for k, v in style_dict.items()])

        # Handle special cases
        if element == 'pre code':
            html_content = html_content.replace('<pre><code', f'<pre style="{style_str}"><code')
            continue
        elif element == 'tr:nth-child(even)':
            continue
        elif element == 'a:hover':
            continue
        elif ',' in element:
            for sub_element in element.split(','):
                html_content = html_content.replace(f'<{sub_element.strip()}',
                                                    f'<{sub_element.strip()} style="{style_str}"')
            continue

        # Regular elements
        html_content = html_content.replace(f'<{element}', f'<{element} style="{style_str}"')

    return html_content