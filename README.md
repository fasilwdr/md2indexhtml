# md2indexhtml

`md2indexhtml` is a Python package designed to simplify the creation of `index.html` files for Odoo modules. It converts Markdown files to HTML with a clean, modern style that integrates well with Odoo's documentation system.

## Features

- Automatically converts Markdown to styled HTML
- Creates `index.html` in the `static/description` directory (Odoo standard location)
- Generates a clean, professional table of contents
- Applies modern, responsive styling without requiring external CSS
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

### Custom Output Path

You can specify a custom output path using the `--output` or `-o` argument:

```bash
md2indexhtml README.md --output /path/to/output/docs.html
# or use the short form
md2indexhtml README.md -o /path/to/output/docs.html
```

This will:
1. Convert your README.md to HTML
2. Create the output directory if it doesn't exist
3. Save the converted file at the specified path

### Custom Title

You can specify a custom title for the HTML document:

```bash
md2indexhtml README.md --title "My Documentation"
```

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

## Output Example

The converted HTML file will include:
- Responsive design
- Table of contents with smooth scrolling
- Syntax highlighting for code blocks
- Modern typography and spacing
- Mobile-friendly layout

## Styling

The package includes a built-in style system that provides:
- Clean, professional typography
- Syntax highlighting for code blocks
- Responsive tables
- Block quotes styling
- Hierarchical heading styles
- Mobile-friendly design

All styles are included inline in the HTML file, so no external CSS files are needed.

## Use with Odoo

This package is specifically designed for Odoo module documentation. When you publish your module, the generated `index.html` in `static/description` will automatically be used as the module's documentation page on the Odoo Apps store.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License.

## Author

Fasil (@fasilwdr)
Email: fasilwdr@hotmail.com