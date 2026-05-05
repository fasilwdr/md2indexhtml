# md2indexhtml

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/md2indexhtml?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/md2indexhtml)

`md2indexhtml` converts Markdown files into beautifully styled, self-contained HTML pages designed for Odoo module description pages. It **automatically detects the type of each section** (Overview, Features, Installation, Configuration, Screenshots, Usage, FAQ, Changelog, …) and applies an appropriate layout — no manual HTML required.

<div align="center">
  <h2>Smart Section Detection</h2>
  <p>Write plain Markdown. Get a professional, responsive Odoo Apps Store page.</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage1.jpg" alt="Overview section rendered as card grid" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage2.jpg" alt="FAQ section rendered as Q&A list" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage3.jpg" alt="Screenshots section rendered as image gallery" width="800"/>
</div>

## Features

- **Section-Type Detection** — each `---`-separated block is identified from its `## heading` and rendered with the right layout automatically
- **Nine built-in section types** — Overview, Features, Installation, Configuration, Screenshots, Usage, Known Issues, FAQ, Changelog
- **Per-section style customisation** — override any CSS class for any section via a JSON config file or Python dict
- **Automatic image handling** — copies local images, resolves `static/description/` prefixes, preserves external URLs
- **Zero external CSS dependencies** — all required styles are inlined; the page is standalone and Odoo Apps Store-safe
- **CLI and Python API** — flexible usage from the command line or from your own scripts

## Installation

```bash
pip install md2indexhtml
```

## Quick Start

```bash
# Convert your module's README.md
cd your_odoo_module
md2indexhtml README.md

# Result: static/description/index.html
```

## Section Type Detection

Sections are delimited by `---` (horizontal rules). The **first `## heading`** inside each block determines the section type:

| Section type    | Detected when the `## heading` contains…       | Layout |
|-----------------|------------------------------------------------|--------|
| `overview`      | overview, about, introduction, intro           | Intro paragraph + h3 card grid |
| `features`      | feature, capabilities, highlights             | h3 card grid |
| `installation`  | install, setup, getting started, requirement  | Centred steps + code blocks |
| `configuration` | config, configuration, settings, option       | Centred steps + code blocks |
| `screenshots`   | screenshot, demo, preview, gallery, screen    | Responsive image gallery |
| `usage`         | usage, how to, guide, tutorial, workflow      | h3 card grid |
| `known_issues`  | known issue, known bug, limitation            | Alert box |
| `faq`           | faq, frequently asked, question               | Q&A list |
| `changelog`     | changelog, change log, release, history       | Version entry cards |
| `generic`       | *(anything else)*                             | Centred content block |

Consecutive `---` blocks with **no `##` heading** inherit the type of the preceding block. This lets you spread a long FAQ or Usage section across multiple `---`-separated sub-blocks.

## Sample Markdown

The following sample shows the full range of supported sections:

```markdown
## Overview

Sample Odoo Module is a lightweight extension built for Odoo 19.

### ⚡ Lightweight & Fast
Minimal footprint with zero performance overhead.

### 🔌 Plug & Play
Install in seconds with no complex configuration.

---

## Features

### 🎯 Feature One
Clean, focused implementation.

### 🔄 Feature Two
Smart automation that keeps your data in sync.

---

## Installation

1. **Download** — Purchase from the Odoo Apps Store.
2. **Place** — Copy the module folder into your addons path.
3. **Install** — Restart Odoo and click Install.

\`\`\`bash
sudo systemctl restart odoo
\`\`\`

---

## Screenshots

![Module overview](static/description/img/screen1.png)
> Main dashboard

![Settings panel](static/description/img/screen2.png)
> Configuration screen

---

## FAQ

**Which Odoo versions are supported?**
Odoo 19.0 Community and Enterprise.

---

**Are there third-party dependencies?**
No, only Odoo's standard `base` module.

---

## Changelog

### v1.0.0 — 2026-05-05
- Initial release
```

## Style Customisation

Every CSS class used in every section is exposed and overridable. You can customise:

- The `<section>` wrapper class
- Heading classes
- Card, grid, figure, alert, FAQ item classes — and more

### Via CLI (JSON file)

Create a JSON file with the section types you want to override:

```json
{
  "overview": {
    "section_class": "o_section_overview py-5 bg-primary text-white",
    "h2_class": "display-4 text-center mb-4 text-white",
    "card_class": "card h-100 border-0 shadow-lg w-100"
  },
  "features": {
    "section_class": "o_section_features py-5",
    "grid_class": "row row-cols-1 row-cols-md-3"
  },
  "faq": {
    "item_class": "faq-item mb-3 p-4 border rounded shadow",
    "question_class": "faq-question h5 font-weight-bold mb-2 text-primary"
  },
  "changelog": {
    "entry_class": "changelog-entry mb-4 p-4 bg-white border-left border-primary rounded"
  }
}
```

Then pass it to the CLI:

```bash
md2indexhtml README.md --style-config my_style.json
```

### Via Python API

```python
from md2indexhtml import convert_md_to_html

convert_md_to_html(
    md_file_path="README.md",
    title="My Module",
    style_config={
        "overview": {
            "section_class": "o_section_overview py-5 bg-dark text-light",
            "h2_class": "display-4 text-center mb-4 text-light",
        },
        "screenshots": {
            "grid_class": "row row-cols-1 row-cols-md-3",
        },
    }
)
```

### Available style keys per section type

Use `md2indexhtml.DEFAULT_SECTION_STYLES` to inspect all available keys:

```python
from md2indexhtml import DEFAULT_SECTION_STYLES
import json
print(json.dumps(DEFAULT_SECTION_STYLES, indent=2))
```

## CLI Reference

```
md2indexhtml [FILE] [OPTIONS]

Arguments:
  FILE                    Path to the Markdown file (optional; auto-detected if omitted)

Options:
  --title TEXT            Document title (default: "Documentation")
  --output / -o PATH      Custom output path (default: static/description/index.html)
  --stylesheet TEXT       Comma-separated stylesheet URLs/paths to inject into <head>
  --script TEXT           Comma-separated script URLs/paths to inject before </body>
  --style-config PATH     Path to a JSON file with per-section-type style overrides
  --version               Show version and exit
```

### Examples

```bash
# Basic conversion
md2indexhtml README.md

# Custom title and output path
md2indexhtml README.md --title "My Odoo Module" --output docs/index.html

# Inject custom stylesheet and script
md2indexhtml README.md --stylesheet "custom.css" --script "analytics.js"

# Apply custom section styles
md2indexhtml README.md --style-config my_style.json

# Get version
md2indexhtml --version
```

## Python API

```python
from md2indexhtml import convert_md_to_html

# Basic conversion
convert_md_to_html("README.md")

# Full options
convert_md_to_html(
    md_file_path="README.md",
    title="My Module",
    output_path="static/description/index.html",
    stylesheets=["https://example.com/extra.css"],
    scripts=["analytics.js"],
    style_config={
        "features": {
            "section_class": "o_section_features py-5 bg-light",
            "card_class": "card h-100 shadow border-0 w-100",
        }
    }
)
```

## How Section Continuation Works

Blocks with no `## heading` inherit the type of the previous block and are merged into the same rendered `<section>`. This is how multi-block FAQ and Usage sections work:

```markdown
## Usage

### Step one
Description of step one.

---

### Step two          ← no ## heading; still "usage"
Description of step two.

---

## Changelog          ← new section type
```

The two usage blocks are combined into a single `<section class="o_section_usage …">` with all their h3 cards side-by-side.

## Output Structure

The generated HTML:

- Is a **complete, standalone HTML document** — self-contained CSS, no external dependencies
- Uses `<section class="o_section_<type> …">` wrappers for each section
- Uses the `.oe_structure` container expected by the Odoo Apps Store renderer
- Includes Google Fonts (Inter) for professional typography
- Is **mobile-responsive** using a lightweight custom grid

## Contributing

```bash
git clone https://github.com/fasilwdr/md2indexhtml.git
cd md2indexhtml
pip install -e .
```

Pull requests and issues are welcome on GitHub.

## License

MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Fasil** (@fasilwdr)
Email: fasilwdr@hotmail.com
GitHub: https://github.com/fasilwdr

---

**Write clean Markdown. Get a professional Odoo Apps Store page — automatically.**
