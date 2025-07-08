# md2indexhtml

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
- **Dictionary-Based Configuration**: Flexible styling system using JSON configuration files
- **Semantic HTML5**: Generates clean, accessible HTML with proper semantic structure
- **Automatic Image Handling**: Processes and copies images with responsive styling
- **Custom Style Configurations**: Override default styling with custom JSON configurations
- **CLI Integration**: Simple command-line interface with powerful options
- **Responsive Design**: Mobile-friendly layouts with Odoo's responsive classes
- **Typography Excellence**: Beautiful typography using Odoo's font system
- **Card-Based Layouts**: Automatic section organization into elegant card layouts
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

### Custom Style Configuration

Create a JSON file with your custom styling preferences:

```json
{
  "h1": {
    "class": "display-2 text-primary text-center mb-5",
    "style": "border-bottom: 3px solid #875A7B;"
  },
  "p": {
    "class": "lead text-muted mb-4"
  },
  "table": {
    "class": "table table-dark table-striped table-hover"
  }
}
```

Then apply it:

```bash
md2indexhtml README.md --style-config my-styles.json
```

### View Default Configuration

See all available styling options:

```bash
md2indexhtml --show-config
```

This displays the complete default Odoo styling configuration organized by categories.

## Configuration System

### Default Odoo Styling

The package comes with comprehensive default styling that covers:

- **Typography**: Headers (h1-h6), paragraphs, emphasis, code blocks
- **Lists**: Unordered, ordered, and definition lists
- **Tables**: Full table styling with headers, borders, and hover effects
- **Forms**: Input fields, buttons, fieldsets with Odoo styling
- **Layout**: Containers, sections, cards, and grid systems
- **Media**: Images, figures, and responsive media elements
- **Navigation**: Navigation bars, breadcrumbs, and links
- **Interactive**: Alerts, badges, progress bars, and tooltips

### Custom Configuration Format

Style configurations use a simple dictionary format:

```python
{
    "element_name": {
        "attribute_name": "attribute_value",
        "class": "css-classes",
        "id": "element-id",
        "style": "inline-css"
    }
}
```

**Examples:**

```json
{
  "h2": {
    "class": "text-center text-primary mb-4",
    "style": "border-bottom: 2px solid #875A7B;"
  },
  "blockquote": {
    "class": "alert alert-info border-left-primary",
    "style": "border-left: 4px solid #17a2b8;"
  },
  "img": {
    "class": "img-fluid rounded shadow-lg mb-4 d-block mx-auto",
    "style": "max-height: 400px;"
  }
}
```

### Styling Categories

The default configuration includes styling for:

1. **Typography Elements**: h1-h6, p, strong, em, small, mark
2. **List Elements**: ul, ol, li, dl, dt, dd
3. **Table Elements**: table, thead, tbody, tr, th, td
4. **Code Elements**: pre, code
5. **Media Elements**: img, figure, figcaption
6. **Layout Elements**: div, section, article, main, aside, header, footer
7. **Form Elements**: form, input, textarea, select, button, fieldset, legend
8. **Interactive Elements**: a, nav, details, summary

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

## Features

- Feature 1
- Feature 2

<div class="alert alert-warning">
    <strong>Note:</strong> Important information here
</div>
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
- Warns about missing images but continues processing

## Python API

Use the package programmatically:

```python
from md2indexhtml import convert_md_to_html

# Basic conversion
convert_md_to_html("README.md")

# With custom configuration
style_config = {
    "h1": {"class": "display-1 text-center text-primary"},
    "p": {"class": "lead mb-4"}
}

convert_md_to_html(
    md_file_path="README.md",
    title="My Documentation",
    output_path="docs/index.html",
    style_config=style_config
)

# Load configuration from file
from md2indexhtml.converter import create_style_config_from_file

config = create_style_config_from_file("styles.json")
convert_md_to_html("README.md", style_config=config)
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

# Apply custom styling
md2indexhtml README.md --style-config custom-styles.json

# View default configuration
md2indexhtml --show-config

# Get version
md2indexhtml --version
```

## Examples

### Basic Module Documentation

```markdown
# Inventory Management Pro

Advanced inventory management for Odoo with real-time tracking.

## Key Features

- Real-time stock tracking
- Automated reorder points
- Advanced reporting dashboard
- Mobile-friendly interface

## Installation

1. Download the module
2. Install in your Odoo instance
3. Configure your settings

## Screenshots

![Dashboard](screenshots/dashboard.png)
![Reports](screenshots/reports.png)
```

### Custom Styling Example

Create `custom-style.json`:

```json
{
  "h1": {
    "class": "display-3 text-center text-primary mb-5",
    "style": "text-shadow: 2px 2px 4px rgba(0,0,0,0.1);"
  },
  "h2": {
    "class": "h3 text-secondary mb-3 border-bottom border-primary pb-2"
  },
  "img": {
    "class": "img-fluid rounded-lg shadow-lg mb-4 d-block mx-auto",
    "style": "border: 3px solid #875A7B;"
  }
}
```

Apply it:

```bash
md2indexhtml README.md --style-config custom-style.json
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