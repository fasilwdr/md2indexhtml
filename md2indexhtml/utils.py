# md2indexhtml/utils.py

import os

def load_template(template_name):
    """
    Load an HTML template from the templates directory.

    :param template_name: Name of the template file (without extension).
    :return: Template content as a string.
    """
    template_path = os.path.join(os.path.dirname(__file__), 'templates', f'{template_name}.html')

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template {template_name} not found.")

    with open(template_path, 'r', encoding='utf-8') as template_file:
        return template_file.read()
