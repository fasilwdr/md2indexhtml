# md2indexhtml

`md2indexhtml` is a Python package designed to simplify the creation of `index.html` files for Odoo modules. It converts Markdown files to HTML with a clean, modern style that integrates well with Odoo's documentation system. The package supports both markdown content and direct HTML sections, allowing for flexible and beautiful documentation.

<div align="center">
  <h2>Package in Action</h2>
  <p>Transform your Markdown documentation into beautiful, styled HTML pages for Odoo modules</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage1.jpg" alt="Clean Documentation Example" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage2.jpg" alt="Modern Styling Example" width="800"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/fasilwdr/md2indexhtml/refs/heads/main/img/sample_usage3.jpg" alt="Professional Layout Example" width="800"/>
</div>

<div align="center">
  <p>Transform your documentation with a single command:</p>
  <pre><code>md2indexhtml README.md</code></pre>
</div>

## Features

- Automatically converts Markdown to styled HTML
- Creates `index.html` in the `static/description` directory (Odoo standard location)
- Supports direct HTML sections in markdown files
- Automatic image handling and migration
- Maintains image directory structure
- Converts markdown headers (#, ##) into styled sections automatically
- Creates responsive card-based layouts for content
- Three template styles: modern, simple, and Odoo-specific
- Bootstrap-based responsive design
- Simple command-line interface
- Flexible output path options

## Installation

Install the package using pip:

```bash
pip install md2indexhtml
```

## Usage

### Basic Usage

The simplest way to use md2indexhtml is to run it in your Odoo module directory:

```bash
cd your_odoo_module
md2indexhtml README.md
```

This will:
1. Convert your README.md to HTML
2. Create a `static/description` directory if it doesn't exist
3. Save the converted file as `index.html` in that directory

### Without Arguments

If you run md2indexhtml without any arguments in a directory containing a markdown file:

```bash
cd your_odoo_module
md2indexhtml
```

It will automatically:
1. Find the first .md file in the current directory
2. Convert it to HTML
3. Save it as `static/description/index.html`

### Custom Title

You can specify a custom title for the HTML document (defaults to "Documentation"):

```bash
md2indexhtml README.md --title "My Documentation"
```

### Custom Output Path

You can specify a custom output path using the `--output` or `-o` argument:

```bash
md2indexhtml README.md --output /path/to/output/docs.html
# or use the short form
md2indexhtml README.md -o /path/to/output/docs.html
```

### Template Styles (New in v0.3.0)

You can now choose between three template styles using the `--template` or `-t` argument:

```bash
# Modern template with Bootstrap styling
md2indexhtml README.md --template modern

# Simple, clean Bootstrap template
md2indexhtml README.md --template simple

# Odoo-specific template optimized for Odoo Apps Store
md2indexhtml README.md --template odoo
```

By default, the Odoo template is used if no style is specified.

### Mixing HTML and Markdown

You can mix direct HTML sections with markdown content in your files:

```markdown
<section style="background: #003554;">
    <!-- Your custom HTML section -->
</section>

# Module Title
## Feature 1
- Feature description
- Another point

<section style="background: linear-gradient(...);">
    <!-- Another HTML section -->
</section>
```

### Image Handling

The package automatically handles images in both Markdown and HTML formats:

```markdown
# Using Markdown syntax
![Alt text](any/path/screenshot.png)

# Using HTML syntax
<img src="path/to/screenshot.png" alt="Alt text">
```
When converting your documentation:

* All local images are automatically copied to an images/ directory in the output path
* Only the filename is kept, discarding the original directory structure
* Image paths in the HTML are updated to point to images/filename.png
* External images (http/https URLs) remain unchanged
* Base64 encoded images are preserved as is
* Missing images generate warnings but don't stop the conversion

For example:

* An image at `screenshots/feature.png` becomes `images/feature.png` in the output
* An image at `assets/img/demo/screenshot.png` becomes `images/screenshot.png`
* An external image `https://example.com/image.jpg` remains unchanged
* A base64 image `data:image/png;base64,...` remains unchanged

### Python API

You can also use the package programmatically in your Python code:

```python
from md2indexhtml import convert_md_to_html

# Convert specific file
convert_md_to_html("README.md")

# Convert with custom output path
convert_md_to_html("README.md", output_path="docs/output.html")

# Convert with custom title
convert_md_to_html("README.md", title="My Documentation")

# Convert with specific template style (new in v0.3.0)
convert_md_to_html("README.md", template_style="modern")

# Or let it find a markdown file automatically
convert_md_to_html()
```

## Output Style

The converted HTML file includes:

- Bootstrap-based responsive design (new in v0.3.0)
- Modern typography with Inter or Montserrat fonts
- Responsive design for all screen sizes
- Syntax highlighting for code blocks
- Clean lists and blockquotes styling
- Mobile-friendly layout
- Three template options to choose from

### Template Styles

#### Modern Template (new in v0.3.0)
- Contemporary styling with gradients and cards
- Montserrat font for headings, Inter for body text
- Hover animations and subtle shadows
- Perfect for feature-rich modules

#### Simple Template (new in v0.3.0)
- Clean, minimalist design
- Lightweight and fast-loading
- Focus on readability and content

#### Odoo Template (new in v0.3.0)
- Specifically designed for Odoo Apps Store integration
- Uses Odoo's color scheme and UI patterns
- Optimized for the marketplace environment

### Markdown Conversion

- `#` headers become full-width sections
- `##` headers become card sections or feature blocks
- Lists, code blocks, and other markdown elements get appropriate styling
- Custom HTML sections are preserved exactly as written

## Use with Odoo

This package is specifically designed for Odoo module documentation. When you publish your module, the generated `index.html` in `static/description` will automatically be used as the module's documentation page on the Odoo Apps store.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License.

## Author

Fasil (@fasilwdr)  
Email: fasilwdr@hotmail.com