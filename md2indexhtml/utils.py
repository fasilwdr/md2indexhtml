# utils.py

import re


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
    content = re.sub(r'<img\s', '<img style="width: 100%;" ', content)

    return content