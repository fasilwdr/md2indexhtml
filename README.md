# md2indexhtml

`md2indexhtml` is a Python package designed to simplify the creation of `index.html` files for Odoo modules. It converts Markdown files to HTML with a clean, modern style that integrates well with Odoo's documentation system. The package supports both markdown content and direct HTML sections, allowing for flexible and beautiful documentation.

## Features

- Automatically converts Markdown to styled HTML
- Creates `index.html` in the `static/description` directory (Odoo standard location)
- Supports direct HTML sections in markdown files
- Automatic image handling and migration
- Maintains image directory structure
- Converts markdown headers (#, ##) into styled sections automatically
- Creates responsive card-based layouts for content
- Applies modern, inline styling without external CSS
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
![Alt text](images/screenshot.png)

# Using HTML syntax
<img src="images/screenshot.png" alt="Alt text">
```
When converting your documentation:

* Local images are automatically copied to the output directory
* Original directory structure is maintained
* Image paths are updated in the generated HTML
* External images (http/https URLs) remain unchanged
* Missing images generate warnings but don't stop the conversion

For example, if your markdown file references an image at `images/screenshots/feature.png`, it will be copied to `static/description/images/screenshots/feature.png` in the output, maintaining the same directory structure.

The converter will preserve your HTML sections exactly as written while converting markdown sections into styled HTML.

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

# Or let it find a markdown file automatically
convert_md_to_html()
```

## Output Style

The converted HTML file includes:

- Gradient backgrounds for main sections
- Card-based layout for subsections
- Modern typography with Inter font
- Responsive design for all screen sizes
- Syntax highlighting for code blocks
- Clean lists and blockquotes styling
- Mobile-friendly layout
- All styles are inline (no external CSS needed)

### Markdown Conversion

- `#` headers become full-width gradient sections
- `##` headers become card sections with white backgrounds
- Lists, code blocks, and other markdown elements get appropriate styling
- Custom HTML sections are preserved exactly as written

## Sample Usages

- ![Sample Usage 1](img/sample_usage1.jpg)
- ![Sample Usage 2](img/sample_usage2.jpg)
- ![Sample Usage 3](img/sample_usage3.jpg)


## Use with Odoo

This package is specifically designed for Odoo module documentation. When you publish your module, the generated `index.html` in `static/description` will automatically be used as the module's documentation page on the Odoo Apps store.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License.

## Author

Fasil (@fasilwdr)  
Email: fasilwdr@hotmail.com