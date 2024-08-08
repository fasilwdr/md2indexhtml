import os
import re


def load_template(template_name):
    """
    Load an HTML template from the templates directory.

    :param template_name: Name of the template file (without extension).
    :return: Template content as a string.
    """
    template_path = os.path.join(os.path.dirname(__file__), 'templates', f'{template_name}')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found.")

    with open(template_path, 'r', encoding='utf-8') as template_file:
        return template_file.read()


def extract_title_and_headers(md_content):
    """
    Extract the title (first header) and generate a sidebar from headers and sub-headers in the Markdown content.

    :param md_content: Markdown content as a string.
    :return: Tuple containing the title and the HTML for the sidebar.
    """
    lines = md_content.split('\n')
    title = ""
    headers_html = "<div class='sidebar'><ul>"

    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            headers_html += f"<li><a href='#{slugify(title)}'>{title}</a></li>"
        elif line.startswith("## "):
            header = line.lstrip("## ").strip()
            headers_html += f"<li class='sub-header'><a href='#{slugify(header)}'>{header}</a></li>"
        elif line.startswith("### "):
            sub_header = line.lstrip("### ").strip()
            headers_html += f"<li class='sub-sub-header'><a href='#{slugify(sub_header)}'>{sub_header}</a></li>"

    headers_html += "</ul></div>"

    return title, headers_html


def slugify(value, separator='-'):
    """
    Convert a string into a slug for use in URLs and IDs.
    :param value: String to be converted to a slug.
    :param separator: Separator to use for spaces.
    :return: Slugified string.
    """
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', separator, value)