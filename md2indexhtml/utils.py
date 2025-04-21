# utils.py

import re
import os
import shutil


def handle_images(content, md_file_path, output_dir):
    """
    Process image paths in content and copy images to output directory
    All local images are copied to images/ directory in output_dir
    Only filenames are kept, discarding original directory structure

    :param content: HTML content
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
    :return: Updated content with new image paths
    """

    def is_local_path(path):
        """Check if the path is a local file path"""
        return not (path.startswith(('http://', 'https://', 'data:', '/web/', 'www.')) or
                    path.startswith('data:image/'))  # Handle base64 images

    def process_image_path(img_path):
        """Process and copy local image if needed"""
        img_path = img_path.strip("'\" ")

        # If the path starts with 'static/description/', just remove the prefix and return
        if img_path.startswith('static/description/'):
            return img_path[18:]  # Remove 'static/description/' prefix

        # Skip non-local paths and base64 images
        if not is_local_path(img_path):
            return img_path

        try:
            # Get absolute paths
            md_dir = os.path.dirname(os.path.abspath(md_file_path))
            abs_img_path = os.path.normpath(os.path.join(md_dir, img_path))

            # Skip if image doesn't exist
            if not os.path.isfile(abs_img_path):
                print(f"Warning: Image not found at {abs_img_path}")
                return img_path

            # Create images directory in output path
            images_dir = os.path.join(output_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)

            # Get just the filename from the path
            filename = os.path.basename(img_path)

            # Copy the image to images directory
            target_path = os.path.join(images_dir, filename)
            shutil.copy2(abs_img_path, target_path)

            # Return the new path relative to output directory - without leading slash
            return f'images/{filename}'  # Removed leading slash

        except Exception as e:
            print(f"Warning: Failed to process image {img_path}: {str(e)}")
            return img_path

    # Handle Markdown image syntax
    def replace_md_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)

        # If it's a base64 image, keep it as is
        if img_path.startswith('data:image/'):
            return f'<img alt="{alt_text}" src="{img_path}" class="img-fluid"/>'

        # Process other images
        new_path = process_image_path(img_path)
        return f'<img alt="{alt_text}" src="{new_path}" class="img-fluid"/>'

    # Handle HTML image syntax
    def replace_html_image(match):
        quote = match.group(1)  # preserve the original quote type
        img_path = match.group(2)

        # If it's a base64 image, keep it as is
        if img_path.startswith('data:image/'):
            return f'src={quote}{img_path}{quote}'

        # Process other images
        new_path = process_image_path(img_path)
        # Make sure the path doesn't start with a slash
        if new_path.startswith('/'):
            new_path = new_path[1:]
        return f'src={quote}{new_path}{quote}'

    # Process Markdown image syntax first
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_image, content)

    # Then process HTML image tags
    content = re.sub(r'src=(["\'])(.*?)\1', replace_html_image, content)

    # Add Bootstrap class to all img tags without a class
    content = re.sub(r'<img(?!\s+class=)([^>]*?)>', r'<img class="img-fluid" \1>', content)

    # Fix any remaining image paths that start with a slash
    content = re.sub(r'src="/images/', r'src="images/', content)

    return content


def wrap_sections(html_content):
    """
    Wrap HTML content in sections based on h1 and h2 tags

    :param html_content: HTML content as string
    :return: Wrapped HTML content
    """
    # Split content by h1 tags
    parts = re.split(r'(<h1.*?</h1>)', html_content, flags=re.DOTALL)

    wrapped_content = []
    for i in range(1, len(parts), 2):
        if i < len(parts):
            h1_content = parts[i]
            following_content = parts[i + 1] if i + 1 < len(parts) else ''

            # Split following content by h2 tags
            h2_parts = re.split(r'(<h2.*?</h2>)', following_content, flags=re.DOTALL)

            # Extract h1 text
            h1_text = re.search(r'>([^<]+)</h1>', h1_content)
            h1_text = h1_text.group(1) if h1_text else ''

            # Create section wrapper
            section = f'''
            <section style="background: linear-gradient(to right, #003554, #52A3AB);border-radius: 20px;max-width: 1200px; margin-bottom: 20px; padding: 20px;margin: 50px auto 20px auto;">
                <div style="text-align: center;">
                    <h1 style="color: white; font-size: 2.5em; margin-bottom: 10px;">{h1_text}</h1>
                </div>
                <div style="border-radius: 10px;display: flex;flex-wrap: wrap;gap: 20px;padding: 20px;">
            '''

            # Process h2 sections
            for j in range(1, len(h2_parts), 2):
                if j < len(h2_parts):
                    h2_content = h2_parts[j]
                    h2_following = h2_parts[j + 1] if j + 1 < len(h2_parts) else ''

                    # Extract h2 text
                    h2_text = re.search(r'>([^<]+)</h2>', h2_content)
                    h2_text = h2_text.group(1) if h2_text else ''

                    # Apply styles for markdown content
                    styled_content = add_markdown_styles(h2_following)

                    section += f'''
                    <div style="background: #fff;box-shadow: 2px 2px 5px 0px #003554;flex: 1 1 calc(50% - 10px);min-width: 280px;">
                        <h2 style="color: #fff; text-align:center; background-color: #52A3AB!important; margin: 0; padding: 15px;">{h2_text}</h2>
                        <div style="padding: 15px;">{styled_content}</div>
                    </div>
                    '''

            section += '''
                </div>
            </section>
            '''

            wrapped_content.append(section)

    return '\n'.join(wrapped_content)


def wrap_sections_bootstrap(html_content):
    """
    Wrap HTML content in bootstrap sections based on h1 and h2 tags
    specifically formatted for Odoo Apps Store compatibility with reliable responsive design

    :param html_content: HTML content as string
    :return: Wrapped HTML content with Bootstrap styling
    """
    # Split content by h1 tags
    parts = re.split(r'(<h1.*?</h1>)', html_content, flags=re.DOTALL)

    # If no h1 tags are found, wrap the entire content
    if len(parts) == 1:
        html_content = add_bootstrap_styles(html_content)
        return f"""<div class="col-lg-12">
            {html_content}
        </div>"""

    wrapped_content = []
    for i in range(1, len(parts), 2):
        if i < len(parts):
            h1_content = parts[i]
            following_content = parts[i + 1] if i + 1 < len(parts) else ''

            # Extract h1 text
            h1_text = re.search(r'>([^<]+)</h1>', h1_content)
            h1_text = h1_text.group(1) if h1_text else ''

            # Create a new section with bootstrap-based h1
            section = f"""<div class="col-lg-12">
                <h2 class="text-center mb-4 mt-4" style="color: #875A7B; font-weight: bold;">{h1_text}</h2>
            """

            # Split following content by h2 tags
            h2_parts = re.split(r'(<h2.*?</h2>)', following_content, flags=re.DOTALL)

            # If there are no h2 tags, wrap all content in a single section
            if len(h2_parts) == 1:
                styled_content = add_bootstrap_styles(following_content)
                section += f"""<div class="mb-4">
                    {styled_content}
                </div>
                """
            else:
                # Process h2 sections for Odoo-style layout
                for j in range(1, len(h2_parts), 2):
                    if j < len(h2_parts):
                        h2_content = h2_parts[j]
                        h2_following = h2_parts[j + 1] if j + 1 < len(h2_parts) else ''

                        # Extract h2 text
                        h2_text = re.search(r'>([^<]+)</h2>', h2_content)
                        h2_text = h2_text.group(1) if h2_text else ''

                        # Apply bootstrap styles for markdown content
                        styled_content = add_bootstrap_styles(h2_following)

                        # Create an Odoo-style section with the h2 content
                        section += f"""<div class="mb-4">
                            <div class="alert alert-info" style="background-color: #F8F9FA; color: #875A7B; border-color: #875A7B; font-weight:300; font-size:20px; border-radius: 5px;">
                                <i class="fa fa-hand-point-right"></i><b> {h2_text}</b>
                            </div>
                            {styled_content}
                        </div>
                        """

            section += """</div>"""
            wrapped_content.append(section)

    return '\n'.join(wrapped_content)


def add_markdown_styles(content):
    """Add inline styles to markdown-generated HTML elements"""
    content = re.sub(r'<h3>', '<h3 style="color: #0A4B75; margin-bottom: 15px;">', content)
    content = re.sub(r'<p>', '<p style="color: #333; line-height: 1.6;">', content)
    content = re.sub(r'<ul>', '<ul style="padding-left: 20px; list-style-type: disc;">', content)
    content = re.sub(r'<li>', '<li style="margin: 5px 0; color: #333;">', content)
    content = re.sub(r'<code>',
                     '<code style="background: #f8f9fa; color: #e74c3c; padding: 2px 5px; border-radius: 3px; font-family: Monaco, Menlo, Ubuntu Mono, Consolas, monospace;">',
                     content)
    content = re.sub(r'<pre>',
                     '<pre style="background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto;">',
                     content)
    content = re.sub(r'<blockquote>',
                     '<blockquote style="border-left: 4px solid #52A3AB; padding: 10px 15px; margin: 10px 0; background: #f7f9fc; color: #34495e;">',
                     content)
    content = re.sub(r'<a\s', '<a style="color: #52A3AB; text-decoration: none;" ', content)
    content = re.sub(r'<img\s', '<img style="max-width: 100%; height: auto;" ', content)

    return content


def add_bootstrap_styles(content):
    """Add Odoo-compatible Bootstrap classes to markdown-generated HTML elements with reliable responsive design"""
    # Headers - Update h3 to be smaller than h2
    content = re.sub(r'<h3>', '<h3 class="mt-3 mb-3" style="color:#875A7B; font-weight: bold; font-size: 1.2rem;">', content)
    content = re.sub(r'<h4>', '<h4 class="mt-3 mb-3" style="color:#875A7B; font-size: 1.1rem;">', content)

    # Paragraphs
    content = re.sub(r'<p>', '<p class="text-justify mb-3" style="color: #555;">', content)

    # Lists
    content = re.sub(r'<ul>', '<ul class="list-unstyled">', content)

    # Convert feature-like list items to Bootstrap cards
    if '• ' in content or '✓ ' in content or re.search(r'<li>[^<]*?(?:Feature|Option|Benefit)[^<]*?</li>', content,
                                                       re.IGNORECASE):
        # Feature list with Bootstrap column grid for responsiveness
        content = re.sub(r'<li>([^<]*?)([Ff]eature|[Oo]ption|[Bb]enefit)([^<]*?)</li>',
                         r'<div class="col-lg-4 col-md-6 mb-4"><div class="card h-100 border-primary"><div class="card-body"><i class="fa fa-check-circle text-primary mr-2"></i><strong>\2</strong>\3</div></div></div>',
                         content)

        # Other feature-like items
        content = re.sub(r'<li>([•✓√] )?([^<]*?)</li>',
                         r'<div class="col-lg-4 col-md-6 mb-4"><div class="card h-100"><div class="card-body"><i class="fa fa-check text-success mr-2"></i> \2</div></div></div>',
                         content)

        # Wrap lists in row
        content = re.sub(r'<ul class="list-unstyled">(.*?)</ul>', r'<div class="row">\1</div>', content,
                         flags=re.DOTALL)
    else:
        # Regular list items
        content = re.sub(r'<li>', '<li class="mb-2"><i class="fa fa-check text-success mr-2"></i> ', content)

    # Ordered lists
    content = re.sub(r'<ol>', '<ol class="pl-3 mb-4">', content)
    content = re.sub(r'<li>([0-9]+\.\s*)', r'<li class="mb-2">\1', content)

    # Code elements
    content = re.sub(r'<code>', '<code class="bg-light text-danger px-1 rounded" style="font-size: 90%;">', content)
    content = re.sub(r'<pre>', '<pre class="bg-light p-3 rounded mb-4 border" style="overflow-x: auto;">', content)

    # Blockquotes
    content = re.sub(r'<blockquote>',
                     '<blockquote class="border-left pl-3 py-2 my-3" style="border-left: 4px solid #875A7B !important; background-color: #f9f9f9;">',
                     content)

    # Links
    content = re.sub(r'<a\s', '<a class="text-primary" ', content)

    # Handle Markdown image syntax before it's converted to HTML
    def fix_markdown_images(match):
        alt_text = match.group(1)
        img_path = match.group(2)

        # Remove static/description prefix if it exists
        if img_path.startswith('static/description/'):
            img_path = img_path[18:]  # removes 'static/description/'
        if img_path.startswith('/'):
            img_path = img_path[1:]  # removes leading slash

        return f'<img class="img-fluid rounded shadow-sm mb-4" alt="{alt_text}" src="{img_path}" />'

    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', fix_markdown_images, content)

    # Fix already converted HTML image tags
    def fix_html_image_tags(match):
        attrs = match.group(1)

        # Extract src attribute
        src_match = re.search(r'src="([^"]+)"', attrs)
        if src_match:
            src = src_match.group(1)
            # Remove static/description prefix if it exists
            if src.startswith('static/description/'):
                src = src[18:]  # removes 'static/description/'
            if src.startswith('/'):
                src = src[1:]  # removes leading slash

            # Replace src in attrs
            attrs = re.sub(r'src="[^"]+"', f'src="{src}"', attrs)

        # Handle class attribute
        if 'class=' in attrs:
            # Replace existing class
            attrs = re.sub(r'class="[^"]*"', 'class="img-fluid rounded shadow-sm mb-4"', attrs)
        else:
            # Add class if it doesn't exist
            attrs += ' class="img-fluid rounded shadow-sm mb-4"'

        # Ensure proper tag closing
        return f'<img {attrs.strip()} />'

    content = re.sub(r'<img([^>]*)>(?!</)', fix_html_image_tags, content)
    content = re.sub(r'<img([^>]*)/>(?!</)', fix_html_image_tags, content)

    # Make sure images are wrapped properly
    def wrap_standalone_images(match):
        img_tag = match.group(0)
        return f'<div class="text-center mb-4">{img_tag}</div>'

    content = re.sub(r'<img[^>]*?/>', wrap_standalone_images, content)

    # Make tables responsive with Bootstrap
    content = re.sub(r'<table>', '<div class="table-responsive mb-4"><table class="table table-bordered table-hover">',
                     content)
    content = re.sub(r'</table>', '</table></div>', content)
    content = re.sub(r'<thead>', '<thead class="thead-light">', content)

    # Ensure buttons use Bootstrap classes
    content = re.sub(r'<button', r'<button class="btn btn-primary"', content)

    # Add Bootstrap classes to any tables
    content = re.sub(r'<table', r'<table class="table table-bordered table-hover"', content)

    return content