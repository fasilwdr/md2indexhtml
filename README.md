# md2indexhtml

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/md2indexhtml?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/md2indexhtml)

`md2indexhtml` is a powerful Python package that converts Markdown files to beautifully styled HTML pages specifically designed for Odoo modules. It uses comprehensive Odoo frontend styling classes from `web.assets_frontend.min.css` to create professional, responsive documentation that integrates seamlessly with Odoo's design system.

<div align="center">
  <h2>Transform Your Documentation</h2>
  <p>Create stunning, professional HTML documentation from Markdown with authentic Odoo styling</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage1.jpg" alt="Professional Odoo Documentation" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage2.jpg" alt="Responsive Design Example" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage3.jpg" alt="Clean Layout Example" width="800"/>
</div>

<div align="center">
  <p>Simple command, beautiful results:</p>
  <pre><code>md2indexhtml README.md</code></pre>
</div>

## Features

- **Comprehensive Odoo Styling**: Uses authentic Odoo frontend classes for consistent design
- **Enhanced Premium Design**: Modern typography (Inter font), soft shadows, and clean card layouts by default
- **Semantic HTML5**: Generates clean, accessible HTML with proper semantic structure
- **Automatic Image Handling**: Processes and copies images with responsive styling
- **Custom Resource Injection**: Easily inject custom CSS stylesheets and JavaScript files
- **CLI Integration**: Simple command-line interface with powerful options
- **Responsive Design**: Mobile-friendly layouts with Odoo's responsive classes
- **Typography Excellence**: Beautiful typography using Odoo's font system alongside Google's Inter font
- **Card-Based Layouts**: Automatic section organization into elegant card layouts with hover effects
- **Table Enhancement**: Professional table styling with striped rows and hover effects

## Installation

Install the package using pip:

```bash
pip install md2indexhtml
```

## Quick Start

### Basic Usage

Convert your README.md to Odoo-styled HTML:

```bash
cd your_odoo_module
md2indexhtml README.md
```

This creates a beautifully styled `static/description/index.html` file perfect for the Odoo Apps Store.

### Without Arguments

If you have a markdown file in your current directory:

```bash
md2indexhtml
```

It automatically finds and converts the first `.md` file found.

## Advanced Usage

### Custom Output Path

Specify where to save the HTML file:

```bash
md2indexhtml README.md --output /path/to/docs.html
# or use the short form
md2indexhtml README.md -o /path/to/docs.html
```

### Custom Title

Set a custom title for your HTML document:

```bash
md2indexhtml README.md --title "Module Documentation"
```

### Inject Custom Styles or Scripts

You can inject custom CSS or JavaScript files into the generated HTML. This is useful for adding google analytics, custom fonts, or specific styling tweaks.

**Add Custom Stylesheet:**
```bash
md2indexhtml README.md --stylesheet "https://fonts.googleapis.com/css?family=Open+Sans,custom.css"
```

**Add Custom Script:**
```bash
md2indexhtml README.md --script "https://example.com/analytics.js,custom_script.js"
```

## Content Structure

### Markdown Conversion

The package intelligently converts markdown elements:

- `# Headers` become full-width sections with Odoo styling
- `## Subheaders` become card-based feature sections
- Lists are styled with Odoo's list classes
- Code blocks get syntax highlighting and proper spacing
- Images are automatically made responsive and centered
- Tables receive full Odoo table styling

### HTML Preservation

You can mix HTML directly in your markdown:

```markdown
# My Module

<section class="py-5 bg-primary text-white text-center">
    <h2>Custom HTML Section</h2>
    <p>This will be preserved exactly as written</p>
</section>
```

### Image Handling

The package automatically processes images:

```markdown
# Using Markdown
![Screenshot](screenshots/feature.png)

# Using HTML
<img src="assets/demo.jpg" alt="Demo" />
```

**Automatic Processing:**
- Copies images to `images/` directory in output location
- Updates paths to use only filenames (flattens directory structure)
- Adds responsive classes automatically
- Preserves external URLs and base64 images

## Python API

Use the package programmatically:

```python
from md2indexhtml import convert_md_to_html

# Basic conversion
convert_md_to_html("README.md")

# With custom custom title and output
convert_md_to_html(
    md_file_path="README.md",
    title="My Documentation",
    output_path="docs/index.html"
)

# With custom stylesheets and scripts
convert_md_to_html(
    md_file_path="README.md",
    stylesheets=["https://example.com/style.css", "custom.css"],
    scripts=["https://example.com/script.js"]
)
```

## Output Features

The generated HTML includes:

- **Semantic Structure**: Proper HTML5 semantic elements
- **Responsive Design**: Mobile-first responsive layout
- **Odoo Integration**: Native Odoo styling classes
- **Typography**: Professional typography with Odoo fonts
- **Accessibility**: ARIA labels and semantic markup
- **Performance**: Optimized CSS and clean HTML structure

### Odoo Apps Store Ready

Files generated with `md2indexhtml` are specifically designed for the Odoo Apps Store:

- Uses `oe_structure` containers for proper Odoo integration
- Includes proper meta tags and viewport settings
- Follows Odoo's design guidelines and color schemes
- Optimized for the Apps Store's rendering system

## CLI Reference

```bash
# Convert with defaults
md2indexhtml README.md

# Custom title and output
md2indexhtml README.md --title "My Module" --output custom.html

# Inject Custom resources
md2indexhtml README.md --stylesheet "style.css" --script "app.js"

# Get version
md2indexhtml --version
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on GitHub.

### Development Setup

```bash
git clone https://github.com/fasilwdr/md2indexhtml.git
cd md2indexhtml
pip install -e .
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

**Fasil** (@fasilwdr)  
Email: fasilwdr@hotmail.com  
GitHub: https://github.com/fasilwdr

---

**Transform your Markdown documentation into professional, Odoo-ready HTML with md2indexhtml!**