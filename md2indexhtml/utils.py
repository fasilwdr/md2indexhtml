# utils.py - Section-type-aware Odoo HTML generation

import re
import os
import shutil
import markdown as _markdown_lib
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Section type detection
# ---------------------------------------------------------------------------

# Keyword lists used to identify each section type from an h2 heading.
SECTION_TYPE_KEYWORDS: Dict[str, List[str]] = {
    "overview":      ["overview", "about", "introduction", "intro"],
    "features":      ["feature", "capabilities", "highlights"],
    "installation":  ["install", "setup", "getting started", "quick start", "requirement"],
    "configuration": ["config", "configuration", "settings", "option"],
    "screenshots":   ["screenshot", "demo", "preview", "gallery", "screen"],
    "usage":         ["usage", "how to", "how-to", "guide", "tutorial", "workflow"],
    "known_issues":  ["known issue", "known bug", "limitation", "known problem"],
    "faq":           ["faq", "frequently asked", "question"],
    "changelog":     ["changelog", "change log", "release", "history", "version"],
}

# ---------------------------------------------------------------------------
# Default per-section-type style configuration
# ---------------------------------------------------------------------------

# Each section type maps to a dict of CSS-class strings for its HTML elements.
# Users can override any key by passing a style_config dict at runtime.
DEFAULT_SECTION_STYLES: Dict[str, Dict[str, str]] = {
    "overview": {
        "section_class":    "o_section_overview py-5",
        "container_class":  "container",
        "h2_class":         "display-4 text-center mb-4 font-weight-bold",
        "intro_class":      "lead text-center mb-5",
        "grid_class":       "row row-cols-1 row-cols-md-3",
        "col_class":        "col mb-4 d-flex",
        "card_class":       "card h-100 shadow-sm border-0 w-100",
        "card_body_class":  "card-body",
        "card_title_class": "card-title h5 font-weight-bold",
        "card_text_class":  "card-text",
    },
    "features": {
        "section_class":    "o_section_features py-5 bg-light",
        "container_class":  "container",
        "h2_class":         "text-center mb-5 font-weight-bold",
        "grid_class":       "row row-cols-1 row-cols-md-2 row-cols-lg-3",
        "col_class":        "col mb-4 d-flex",
        "card_class":       "card h-100 shadow-sm border-0 w-100",
        "card_body_class":  "card-body",
        "card_title_class": "card-title h5 font-weight-bold",
        "card_text_class":  "card-text",
    },
    "installation": {
        "section_class":    "o_section_installation py-5",
        "container_class":  "container",
        "h2_class":         "text-center mb-4 font-weight-bold",
        "content_class":    "col-lg-8 mx-auto",
    },
    "configuration": {
        "section_class":    "o_section_configuration py-5 bg-light",
        "container_class":  "container",
        "h2_class":         "text-center mb-4 font-weight-bold",
        "content_class":    "col-lg-8 mx-auto",
    },
    "screenshots": {
        "section_class":    "o_section_screenshots py-5",
        "container_class":  "container",
        "h2_class":         "text-center mb-5 font-weight-bold",
        "grid_class":       "row row-cols-1 row-cols-md-2",
        "col_class":        "col mb-4",
        "figure_class":     "figure w-100",
        "img_class":        "figure-img img-fluid rounded shadow w-100",
        "caption_class":    "figure-caption text-center text-muted mt-2 d-block",
    },
    "usage": {
        "section_class":    "o_section_usage py-5 bg-light",
        "container_class":  "container",
        "h2_class":         "text-center mb-5 font-weight-bold",
        "grid_class":       "row row-cols-1 row-cols-md-2 row-cols-lg-3",
        "col_class":        "col mb-4 d-flex",
        "card_class":       "card h-100 shadow-sm border-0 w-100",
        "card_body_class":  "card-body",
        "card_title_class": "card-title h5 font-weight-bold",
        "card_text_class":  "card-text",
    },
    "known_issues": {
        "section_class":    "o_section_known_issues py-4",
        "container_class":  "container",
        "h2_class":         "text-center mb-4 font-weight-bold",
        "content_class":    "col-lg-8 mx-auto",
        "alert_class":      "alert alert-warning",
    },
    "faq": {
        "section_class":    "o_section_faq py-5",
        "container_class":  "container",
        "h2_class":         "text-center mb-5 font-weight-bold",
        "content_class":    "col-lg-8 mx-auto",
        "item_class":       "faq-item mb-4 p-3 bg-light rounded shadow-sm",
        "question_class":   "faq-question h5 font-weight-bold mb-2",
        "answer_class":     "faq-answer mb-0",
    },
    "changelog": {
        "section_class":    "o_section_changelog py-5 bg-light",
        "container_class":  "container",
        "h2_class":         "text-center mb-5 font-weight-bold",
        "content_class":    "col-lg-8 mx-auto",
        "entry_class":      "changelog-entry mb-4 p-3 bg-white rounded shadow-sm",
        "version_class":    "changelog-version h5 font-weight-bold text-primary mb-2",
    },
    "generic": {
        "section_class":    "o_section_generic py-4",
        "container_class":  "container",
        "h2_class":         "text-center mb-4 font-weight-bold",
        "content_class":    "col-lg-10 mx-auto",
    },
}

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

_MD_EXTENSIONS = ["tables", "fenced_code", "codehilite", "nl2br", "sane_lists", "attr_list"]


def _md_to_html(text: str) -> str:
    """Convert a Markdown string to HTML."""
    return _markdown_lib.markdown(text, extensions=_MD_EXTENSIONS)


def detect_section_type(heading_text: str) -> str:
    """
    Detect the section type from an h2 heading string.

    :param heading_text: Plain text of the h2 heading (emoji and extra whitespace stripped).
    :return: One of the keys in SECTION_TYPE_KEYWORDS, or 'generic'.
    """
    # Normalise: lower-case, strip emoji / punctuation that are not word chars or spaces
    clean = re.sub(r'[^\w\s]', ' ', heading_text.lower()).strip()
    for section_type, keywords in SECTION_TYPE_KEYWORDS.items():
        if any(kw in clean for kw in keywords):
            return section_type
    return "generic"


def handle_images(content: str, md_file_path: str, output_dir: str) -> str:
    """
    Process image paths in markdown/HTML content and copy local images to the
    output directory.  All local images are placed in an ``images/`` sub-directory
    inside *output_dir*, and the references are updated accordingly.

    :param content: Markdown or HTML content string.
    :param md_file_path: Absolute path to the source markdown file.
    :param output_dir: Directory where the output HTML will be written.
    :return: Content string with updated image paths.
    """

    def is_local_path(path: str) -> bool:
        return not path.startswith(('http://', 'https://', 'data:', '/web/', 'www.'))

    def process_image_path(img_path: str) -> str:
        img_path = img_path.strip("'\" ")
        # Strip the static/description/ prefix used in Odoo module trees
        if img_path.startswith('static/description/'):
            img_path = img_path[len('static/description/'):]

        if not is_local_path(img_path):
            return img_path

        try:
            md_dir = os.path.dirname(os.path.abspath(md_file_path))
            abs_img_path = os.path.normpath(os.path.join(md_dir, img_path))
            if not os.path.isfile(abs_img_path):
                print(f"Warning: Image not found at {abs_img_path}")
                return img_path
            images_dir = os.path.join(output_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)
            filename = os.path.basename(img_path)
            shutil.copy2(abs_img_path, os.path.join(images_dir, filename))
            return f'images/{filename}'
        except Exception as exc:
            print(f"Warning: Failed to process image {img_path}: {exc}")
            return img_path

    # Markdown image syntax → bare <img> tag (so markdown library won't re-process it)
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        lambda m: f'<img alt="{m.group(1)}" src="{process_image_path(m.group(2))}"/>',
        content,
    )
    # HTML src="..." attributes
    content = re.sub(
        r'src=(["\'])(.*?)\1',
        lambda m: f'src="{process_image_path(m.group(2))}"',
        content,
    )
    return content

# ---------------------------------------------------------------------------
# Document parsing
# ---------------------------------------------------------------------------


def parse_document(content: str) -> List[Dict]:
    """
    Split a Markdown document into a list of section dicts.

    The document is first split on ``---`` (horizontal-rule) separators, then
    each resulting block is further split on ``## heading`` lines.  Every
    resulting sub-block becomes one entry::

        {
            "type":     str,   # detected section type (or inherited from prev)
            "h2_text":  str | None,
            "content":  str,   # markdown text below the h2 (or the whole block)
        }

    :param content: Full markdown file content.
    :return: Ordered list of section dicts.
    """
    raw_blocks = re.split(r'\n[ \t]*---+[ \t]*\n', content)
    sections: List[Dict] = []
    previous_type = "generic"

    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue

        # Split the block on h2 lines
        h2_split = re.split(r'(^##[ \t]+.+)$', block, flags=re.MULTILINE)

        # Content that appears before the first h2 in this block
        pre_h2 = h2_split[0].strip()
        if pre_h2:
            sections.append({
                "type":    previous_type,
                "h2_text": None,
                "content": pre_h2,
            })

        # Walk the (h2_line, body) pairs
        for idx in range(1, len(h2_split), 2):
            h2_line = h2_split[idx].strip()
            body = h2_split[idx + 1].strip() if idx + 1 < len(h2_split) else ""
            h2_text = re.sub(r'^##[ \t]+', '', h2_line).strip()
            section_type = detect_section_type(h2_text)
            previous_type = section_type
            sections.append({
                "type":    section_type,
                "h2_text": h2_text,
                "content": body,
            })

    return sections


def group_sections(sections: List[Dict]) -> List[Dict]:
    """
    Merge consecutive sections that share the same type into a single group.

    :param sections: Output of :func:`parse_document`.
    :return: List of group dicts ``{"type": str, "sections": [...]}``.
    """
    groups: List[Dict] = []
    for sec in sections:
        if groups and groups[-1]["type"] == sec["type"]:
            groups[-1]["sections"].append(sec)
        else:
            groups.append({"type": sec["type"], "sections": [sec]})
    return groups

# ---------------------------------------------------------------------------
# Section renderers
# ---------------------------------------------------------------------------


def _extract_h3_items(html: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Split HTML at <h3> boundaries.

    :return: (intro_html, [(h3_text, body_html), ...])
    """
    parts = re.split(r'(<h3[^>]*>.*?</h3>)', html, flags=re.DOTALL)
    intro = parts[0].strip()
    items: List[Tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        h3_html = parts[i]
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        h3_text = re.sub(r'<[^>]+>', '', h3_html).strip()
        items.append((h3_text, body))
    return intro, items


def _render_cards_section(section_type: str, h2_text: Optional[str],
                          all_md: str, style: Dict[str, str]) -> str:
    """Render an overview, features or usage section as a card grid."""
    html_body = _md_to_html(all_md)
    intro_html, items = _extract_h3_items(html_body)

    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    intro_block = (
        f'<p class="{style.get("intro_class", "")}">'
        f'{re.sub(r"</?p[^>]*>", "", intro_html).strip()}</p>'
        if intro_html else ""
    )

    if not items:
        # No h3 cards – render as a plain content block
        content_class = style.get("content_class", "col-lg-10 mx-auto")
        return (
            f'<section class="{style["section_class"]}">'
            f'<div class="{style["container_class"]}">'
            f'{h2_block}{intro_block}'
            f'<div class="{content_class}">{html_body}</div>'
            f'</div></section>'
        )

    cards_html = ""
    for h3_text, body in items:
        cards_html += (
            f'<div class="{style["col_class"]}">'
            f'<div class="{style["card_class"]}">'
            f'<div class="{style["card_body_class"]}">'
            f'<h3 class="{style["card_title_class"]}">{h3_text}</h3>'
            f'<div class="{style["card_text_class"]}">{body}</div>'
            f'</div></div></div>'
        )

    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}{intro_block}'
        f'<div class="{style["grid_class"]}">{cards_html}</div>'
        f'</div></section>'
    )


def _render_steps_section(section_type: str, h2_text: Optional[str],
                           all_md: str, style: Dict[str, str]) -> str:
    """Render an installation or configuration section as a centred content block."""
    html_body = _md_to_html(all_md)
    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    content_class = style.get("content_class", "col-lg-8 mx-auto")
    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{content_class}">{html_body}</div>'
        f'</div></section>'
    )


def _render_screenshots_section(h2_text: Optional[str],
                                 all_md: str, style: Dict[str, str]) -> str:
    """
    Render a screenshots section as an image gallery grid.

    Images may have been pre-processed by handle_images, so they appear as
    ``<img … />`` tags in the markdown.  Blockquote lines immediately after an
    image are used as figure captions.
    """
    html_body = _md_to_html(all_md)

    # Split on <img …/> or <img …>
    img_split = re.split(r'(<img\b[^>]*/?>)', html_body, flags=re.DOTALL)

    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )

    if len(img_split) < 3:
        # No images found – fall back to plain content
        content_class = style.get("content_class", "col-lg-10 mx-auto")
        return (
            f'<section class="{style["section_class"]}">'
            f'<div class="{style["container_class"]}">'
            f'{h2_block}'
            f'<div class="{content_class}">{html_body}</div>'
            f'</div></section>'
        )

    cols_html = ""
    for i in range(1, len(img_split), 2):
        raw_img = img_split[i]
        following = img_split[i + 1] if i + 1 < len(img_split) else ""

        # Update img classes
        if 'class=' in raw_img:
            img_tag = re.sub(r'class="[^"]*"', f'class="{style["img_class"]}"', raw_img)
        else:
            img_tag = raw_img.rstrip('>').rstrip('/') + f' class="{style["img_class"]}"/>'

        # Caption from the first blockquote that immediately follows
        caption_match = re.search(
            r'(?:^|</p>)\s*<blockquote>\s*<p>(.*?)</p>\s*</blockquote>',
            following, flags=re.DOTALL
        )
        if caption_match:
            caption = re.sub(r'<[^>]+>', '', caption_match.group(1)).strip()
        else:
            alt_match = re.search(r'alt="([^"]*)"', raw_img)
            caption = alt_match.group(1) if alt_match else ""

        cols_html += (
            f'<div class="{style["col_class"]}">'
            f'<figure class="{style["figure_class"]}">'
            f'{img_tag}'
            f'<figcaption class="{style["caption_class"]}">{caption}</figcaption>'
            f'</figure></div>'
        )

    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{style["grid_class"]}">{cols_html}</div>'
        f'</div></section>'
    )


def _render_known_issues_section(h2_text: Optional[str],
                                  all_md: str, style: Dict[str, str]) -> str:
    """Render a known-issues section with alert-box styling."""
    html_body = _md_to_html(all_md)
    # Unwrap any blockquote wrappers and place content inside an alert
    inner = re.sub(r'</?blockquote[^>]*>', '', html_body).strip()
    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    alert_class = style.get("alert_class", "alert alert-warning")
    content_class = style.get("content_class", "col-lg-8 mx-auto")
    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{content_class}">'
        f'<div class="{alert_class}">{inner}</div>'
        f'</div></div></section>'
    )


def _render_faq_section(h2_text: Optional[str],
                         group_sections_list: List[Dict],
                         style: Dict[str, str]) -> str:
    """
    Render all consecutive FAQ blocks as a single Q&A list.

    Each section-dict's content is treated as one FAQ entry; the first
    ``<strong>`` in the content becomes the question, and the rest is the
    answer.
    """
    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    content_class = style.get("content_class", "col-lg-8 mx-auto")

    items_html = ""
    for sec in group_sections_list:
        if not sec["content"].strip():
            continue
        html = _md_to_html(sec["content"])
        # Extract the first <strong>…</strong> as the question
        q_match = re.search(r'<strong>(.*?)</strong>', html, re.DOTALL)
        if q_match:
            question = q_match.group(1).strip()
            # Everything after the closing </strong> block is the answer
            after_q = html[q_match.end():].strip()
            # Strip a bare </p> that may be left at the start
            after_q = re.sub(r'^</p>', '', after_q).strip()
            answer_html = after_q if after_q else ""
        else:
            question = ""
            answer_html = html

        q_block = (
            f'<p class="{style["question_class"]}">{question}</p>'
            if question else ""
        )
        a_block = (
            f'<div class="{style["answer_class"]}">{answer_html}</div>'
            if answer_html else ""
        )
        items_html += (
            f'<div class="{style["item_class"]}">{q_block}{a_block}</div>'
        )

    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{content_class}">{items_html}</div>'
        f'</div></section>'
    )


def _render_changelog_section(h2_text: Optional[str],
                               all_md: str, style: Dict[str, str]) -> str:
    """
    Render a changelog section as a list of version-entry cards.

    Each ``### version`` heading starts a new entry card.
    """
    html_body = _md_to_html(all_md)
    h3_split = re.split(r'(<h3[^>]*>.*?</h3>)', html_body, flags=re.DOTALL)

    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    content_class = style.get("content_class", "col-lg-8 mx-auto")

    if len(h3_split) < 3:
        # No h3 entries – plain content
        return (
            f'<section class="{style["section_class"]}">'
            f'<div class="{style["container_class"]}">'
            f'{h2_block}'
            f'<div class="{content_class}">{html_body}</div>'
            f'</div></section>'
        )

    entries_html = ""
    for i in range(1, len(h3_split), 2):
        version_html = h3_split[i]
        body = h3_split[i + 1].strip() if i + 1 < len(h3_split) else ""
        version_text = re.sub(r'<[^>]+>', '', version_html).strip()
        entries_html += (
            f'<div class="{style["entry_class"]}">'
            f'<h3 class="{style["version_class"]}">{version_text}</h3>'
            f'{body}</div>'
        )

    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{content_class}">{entries_html}</div>'
        f'</div></section>'
    )


def _render_generic_section(h2_text: Optional[str],
                             all_md: str, style: Dict[str, str]) -> str:
    """Render any unrecognised section as a simple centred content block."""
    html_body = _md_to_html(all_md)
    h2_block = (
        f'<h2 class="{style["h2_class"]}">{h2_text}</h2>' if h2_text else ""
    )
    content_class = style.get("content_class", "col-lg-10 mx-auto")
    return (
        f'<section class="{style["section_class"]}">'
        f'<div class="{style["container_class"]}">'
        f'{h2_block}'
        f'<div class="{content_class}">{html_body}</div>'
        f'</div></section>'
    )

# ---------------------------------------------------------------------------
# Group renderer (dispatches to the correct per-type renderer)
# ---------------------------------------------------------------------------


def render_section_group(group: Dict, style_config: Optional[Dict] = None) -> str:
    """
    Render one section group to an HTML ``<section>`` block.

    :param group: A group dict produced by :func:`group_sections`.
    :param style_config: Optional mapping of section-type → style overrides.
    :return: HTML string for the section.
    """
    if style_config is None:
        style_config = {}
    section_type = group["type"]
    base_style = dict(DEFAULT_SECTION_STYLES.get(section_type,
                                                  DEFAULT_SECTION_STYLES["generic"]))
    base_style.update(style_config.get(section_type, {}))

    sections_list = group["sections"]
    h2_text = next((s["h2_text"] for s in sections_list if s["h2_text"]), None)

    if section_type == "faq":
        return _render_faq_section(h2_text, sections_list, base_style)

    # For all other types, combine all block contents into one markdown string
    all_md = "\n\n".join(s["content"] for s in sections_list if s["content"])

    if section_type in ("overview", "features", "usage"):
        return _render_cards_section(section_type, h2_text, all_md, base_style)
    if section_type in ("installation", "configuration"):
        return _render_steps_section(section_type, h2_text, all_md, base_style)
    if section_type == "screenshots":
        return _render_screenshots_section(h2_text, all_md, base_style)
    if section_type == "known_issues":
        return _render_known_issues_section(h2_text, all_md, base_style)
    if section_type == "changelog":
        return _render_changelog_section(h2_text, all_md, base_style)
    return _render_generic_section(h2_text, all_md, base_style)

# ---------------------------------------------------------------------------
# HTML document wrapper
# ---------------------------------------------------------------------------


def build_html_document(
        sections_html: str,
        title: str,
        stylesheets: Optional[List[str]] = None,
        scripts: Optional[List[str]] = None,
) -> str:
    """
    Wrap rendered section HTML in a complete, self-contained HTML document.

    :param sections_html: Pre-rendered ``<section>`` blocks.
    :param title: ``<title>`` content.
    :param stylesheets: Optional list of external stylesheet URLs to inject.
    :param scripts: Optional list of external script URLs to inject.
    :return: Full HTML document string.
    """
    css_tags = ""
    if stylesheets:
        for css in stylesheets:
            css_tags += f'    <link rel="stylesheet" href="{css}">\n'

    js_tags = ""
    if scripts:
        for js in scripts:
            js_tags += f'    <script src="{js}"></script>\n'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Generated by md2indexhtml">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{css_tags}    <style>
        *, *::before, *::after {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                         "Helvetica Neue", Arial, sans-serif;
            font-size: 1rem;
            line-height: 1.6;
            color: #212529;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}
        .oe_structure {{ width: 100%; }}
        /* ---- Grid ---- */
        .container {{ width: 100%; max-width: 1140px; margin-right: auto; margin-left: auto; padding-right: 1rem; padding-left: 1rem; }}
        .row {{ display: flex; flex-wrap: wrap; margin-right: -0.75rem; margin-left: -0.75rem; }}
        .col {{ flex: 1 0 0%; padding-right: 0.75rem; padding-left: 0.75rem; }}
        .row-cols-1 > * {{ flex: 0 0 100%; max-width: 100%; padding-right: 0.75rem; padding-left: 0.75rem; }}
        @media (min-width: 576px) {{
            .row-cols-md-2 > * {{ flex: 0 0 50%; max-width: 50%; padding-right: 0.75rem; padding-left: 0.75rem; }}
        }}
        @media (min-width: 768px) {{
            .row-cols-md-2 > * {{ flex: 0 0 50%; max-width: 50%; }}
            .row-cols-md-3 > * {{ flex: 0 0 33.333%; max-width: 33.333%; }}
            .col-lg-8 {{ flex: 0 0 66.666%; max-width: 66.666%; }}
            .col-lg-10 {{ flex: 0 0 83.333%; max-width: 83.333%; }}
        }}
        @media (min-width: 992px) {{
            .row-cols-lg-3 > * {{ flex: 0 0 33.333%; max-width: 33.333%; }}
        }}
        .mx-auto {{ margin-right: auto !important; margin-left: auto !important; }}
        .d-flex {{ display: flex !important; }}
        .h-100 {{ height: 100% !important; }}
        .w-100 {{ width: 100% !important; }}
        /* ---- Spacing ---- */
        .py-4 {{ padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; }}
        .py-5 {{ padding-top: 3rem !important; padding-bottom: 3rem !important; }}
        .mb-2 {{ margin-bottom: 0.5rem !important; }}
        .mb-4 {{ margin-bottom: 1.5rem !important; }}
        .mb-5 {{ margin-bottom: 3rem !important; }}
        .mt-2 {{ margin-top: 0.5rem !important; }}
        .p-3  {{ padding: 1rem !important; }}
        /* ---- Typography ---- */
        .display-4 {{ font-size: 2.5rem; font-weight: 700; line-height: 1.2; }}
        .h5 {{ font-size: 1.1rem; font-weight: 600; }}
        .lead {{ font-size: 1.15rem; font-weight: 400; }}
        .text-center {{ text-align: center !important; }}
        .text-muted {{ color: #6c757d !important; }}
        .text-primary {{ color: #0d6efd !important; }}
        .font-weight-bold {{ font-weight: 700 !important; }}
        /* ---- Card ---- */
        .card {{
            position: relative;
            display: flex;
            flex-direction: column;
            background-color: #fff;
            border: 1px solid rgba(0,0,0,.125);
            border-radius: 0.5rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important; }}
        .card-body {{ flex: 1 1 auto; padding: 1.25rem; }}
        .card-title {{ margin-bottom: 0.5rem; }}
        .card-text {{ color: #495057; }}
        .shadow-sm {{ box-shadow: 0 .125rem .25rem rgba(0,0,0,.075) !important; }}
        .border-0 {{ border: 0 !important; }}
        .rounded {{ border-radius: 0.375rem !important; }}
        /* ---- Alert ---- */
        .alert {{ padding: 1rem 1.25rem; border: 1px solid transparent; border-radius: 0.375rem; }}
        .alert-warning {{ color: #664d03; background-color: #fff3cd; border-color: #ffecb5; }}
        /* ---- Background ---- */
        .bg-light {{ background-color: #f8f9fa !important; }}
        .bg-white {{ background-color: #fff !important; }}
        /* ---- Figure / Images ---- */
        .figure {{ display: block; }}
        .figure-img {{ display: block; max-width: 100%; height: auto; }}
        .figure-caption {{ font-size: 0.875rem; }}
        .img-fluid {{ max-width: 100%; height: auto; }}
        /* ---- Code ---- */
        pre {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 0.375rem; padding: 1rem; overflow-x: auto; margin-bottom: 1rem; }}
        code {{ font-size: 0.875em; color: #d63384; background: #f8f9fa; padding: 0.2em 0.4em; border-radius: 0.25rem; }}
        pre code {{ color: inherit; background: none; padding: 0; }}
        /* ---- Misc ---- */
        .faq-question {{ border-bottom: 2px solid #0d6efd; padding-bottom: 0.25rem; }}
        .changelog-version {{ border-left: 4px solid #0d6efd; padding-left: 0.75rem; }}
        blockquote {{ border-left: 4px solid #dee2e6; padding: 0.5rem 1rem; color: #6c757d; margin: 0 0 1rem; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 1rem; }}
        th, td {{ padding: 0.5rem 0.75rem; border: 1px solid #dee2e6; text-align: left; }}
        thead {{ background-color: #e9ecef; }}
        ul, ol {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
        li {{ margin-bottom: 0.25rem; }}
        a {{ color: #0d6efd; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        p {{ margin-top: 0; margin-bottom: 1rem; }}
        h1, h2, h3, h4, h5, h6 {{ margin-top: 0; margin-bottom: 0.5rem; font-weight: 600; line-height: 1.2; }}
    </style>
</head>
<body>
    <div class="oe_structure">
{sections_html}
    </div>
{js_tags}</body>
</html>'''


# Keep legacy alias so any direct imports of wrap_sections_odoo still work.
def wrap_sections_odoo(
        content: str,
        title: str,
        stylesheets: Optional[List[str]] = None,
        scripts: Optional[List[str]] = None,
) -> str:  # pragma: no cover
    return build_html_document(content, title, stylesheets, scripts)