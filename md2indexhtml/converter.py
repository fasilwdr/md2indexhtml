# converter.py

import os
import sys
import json
import argparse
from typing import Optional, Dict, List
from .utils import (
    parse_document,
    group_sections,
    render_section_group,
    handle_images,
    build_html_document,
    DEFAULT_SECTION_STYLES,
)

__version__ = "0.7.0"


def process_md(
        content: str,
        md_file_path: str,
        output_dir: str,
        style_config: Optional[Dict] = None,
) -> str:
    """
    Convert a Markdown string to a fully styled HTML body (``<section>`` blocks).

    Pipeline:
    1. Apply image path handling to the raw markdown.
    2. Parse the document into typed section blocks.
    3. Group consecutive same-typed blocks.
    4. Render each group to HTML.

    :param content: Raw markdown text.
    :param md_file_path: Absolute path to the source file (used for image lookup).
    :param output_dir: Where the output HTML will be written (used for image copy).
    :param style_config: Optional per-section-type style overrides.
    :return: Concatenated HTML ``<section>`` blocks.
    """
    if style_config is None:
        style_config = {}

    # Step 1 – resolve image paths in the markdown source
    content = handle_images(content, md_file_path, output_dir)

    # Step 2 – parse into section dicts
    sections = parse_document(content)

    # Step 3 – group consecutive same-type sections
    groups = group_sections(sections)

    # Step 4 – render each group
    html_parts = [render_section_group(g, style_config) for g in groups]
    return "\n".join(html_parts)


def convert_md_to_html(
        md_file_path: Optional[str] = None,
        title: str = "Documentation",
        output_path: Optional[str] = None,
        stylesheets: Optional[List[str]] = None,
        scripts: Optional[List[str]] = None,
        style_config: Optional[Dict] = None,
) -> str:
    """
    Convert a Markdown file to a styled HTML file.

    :param md_file_path: Path to the Markdown file (auto-discovered if omitted).
    :param title: ``<title>`` value for the HTML document.
    :param output_path: Where to write the HTML file (defaults to
        ``static/description/index.html`` next to the source file).
    :param stylesheets: Extra stylesheet URLs/paths to inject into ``<head>``.
    :param scripts: Extra script URLs/paths to inject before ``</body>``.
    :param style_config: Per-section-type style overrides (see
        :data:`~md2indexhtml.utils.DEFAULT_SECTION_STYLES`).
    :return: Absolute path to the generated HTML file.
    """
    try:
        # Resolve markdown file path
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

        # Resolve output path
        if output_path:
            output_path = os.path.abspath(output_path)
            output_dir = os.path.dirname(output_path)
        else:
            output_dir = os.path.join(os.path.dirname(md_file_path), 'static', 'description')
            output_path = os.path.join(output_dir, 'index.html')

        os.makedirs(output_dir, exist_ok=True)

        with open(md_file_path, 'r', encoding='utf-8') as fh:
            content = fh.read()

        sections_html = process_md(content, md_file_path, output_dir, style_config)
        html_output = build_html_document(sections_html, title, stylesheets, scripts)

        with open(output_path, 'w', encoding='utf-8') as fh:
            fh.write(html_output)

        print(f"Successfully converted {md_file_path} to {output_path}")
        return output_path

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert Markdown files to styled HTML for Odoo modules. "
            "Section types are auto-detected from ## headings and rendered "
            "with appropriate layouts (cards, steps, gallery, FAQ, …)."
        )
    )
    parser.add_argument('file', nargs='?', help='Path to the Markdown file (optional)')
    parser.add_argument('--version', action='version', version=f'md2indexhtml {__version__}')
    parser.add_argument('--title', default="Documentation",
                        help='Custom title for the HTML document')
    parser.add_argument('--output', '-o', help='Custom output path for the HTML file')
    parser.add_argument('--stylesheet',
                        help='Comma-separated stylesheet URLs/paths to inject')
    parser.add_argument('--script',
                        help='Comma-separated script URLs/paths to inject')
    parser.add_argument('--style-config',
                        help=(
                            'Path to a JSON file with per-section-type style overrides. '
                            'Keys are section types (overview, features, installation, '
                            'configuration, screenshots, usage, known_issues, faq, '
                            'changelog, generic); values are dicts of CSS-class strings '
                            'matching the keys in DEFAULT_SECTION_STYLES.'
                        ))

    args = parser.parse_args()

    stylesheets = (
        [s.strip() for s in args.stylesheet.split(',') if s.strip()]
        if args.stylesheet else None
    )
    scripts = (
        [s.strip() for s in args.script.split(',') if s.strip()]
        if args.script else None
    )

    style_config: Optional[Dict] = None
    if args.style_config:
        cfg_path = os.path.abspath(args.style_config)
        if not os.path.exists(cfg_path):
            print(f"Error: style-config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(1)
        with open(cfg_path, 'r', encoding='utf-8') as fh:
            style_config = json.load(fh)

    convert_md_to_html(
        md_file_path=args.file,
        title=args.title,
        output_path=args.output,
        stylesheets=stylesheets,
        scripts=scripts,
        style_config=style_config,
    )


if __name__ == '__main__':
    main()