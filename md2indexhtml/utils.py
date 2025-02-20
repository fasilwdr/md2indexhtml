# utils.py

import re
import os
import shutil


def handle_images(content, md_file_path, output_dir):
    """
    Process image paths in content and copy images to output directory

    :param content: HTML content
    :param md_file_path: Path to original markdown file
    :param output_dir: Output directory path
    :return: Updated content with new image paths
    """

    def is_local_path(path):
        """Check if the path is a local file path"""
        return not path.startswith(('http://', 'https://', 'data:', '/web/', 'www.'))

    def process_image_path(img_path):
        """Process and copy local image if needed"""
        img_path = img_path.strip("'\" ")

        # Skip non-local paths
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

            # Create target directory structure
            rel_dir = os.path.dirname(img_path)
            if rel_dir:
                target_dir = os.path.join(output_dir, rel_dir)
                os.makedirs(target_dir, exist_ok=True)

            # Copy the image
            target_path = os.path.join(output_dir, img_path)
            shutil.copy2(abs_img_path, target_path)

            return img_path

        except Exception as e:
            print(f"Warning: Failed to process image {img_path}: {str(e)}")
            return img_path

    # Handle Markdown image syntax
    def replace_md_image(match):
        alt_text = match.group(1)
        img_path = process_image_path(match.group(2))
        return f'<img alt="{alt_text}" src="{img_path}"/>'

    # Handle HTML image syntax
    def replace_html_image(match):
        quote = match.group(1)  # preserve the original quote type
        img_path = process_image_path(match.group(2))
        return f'src={quote}{img_path}{quote}'

    # Process Markdown image syntax first
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_image, content)

    # Then process HTML image tags
    content = re.sub(r'src=(["\'])(.*?)\1', replace_html_image, content)

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