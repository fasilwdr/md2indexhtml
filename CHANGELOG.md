# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-05-05

### Added
- **Section-type detection** — each `---`-separated block is automatically identified
  from its `## heading` (overview, features, installation, configuration, screenshots,
  usage, known_issues, faq, changelog, generic) and rendered with an appropriate layout
- **Per-section-type style customisation** via a JSON config file (`--style-config`) or
  the new `style_config` parameter in the Python API
- **Nine layout renderers**: card grid (overview, features, usage), centred steps
  (installation, configuration), image gallery (screenshots), alert box (known_issues),
  Q&A list (faq), version cards (changelog), plain content (generic)
- `SECTION_TYPE_KEYWORDS` and `DEFAULT_SECTION_STYLES` are now exported from the
  package for programmatic inspection and extension
- Section continuation: `---` blocks with no `##` heading inherit the previous section
  type, enabling multi-block FAQ and Usage sections

### Changed
- **BREAKING**: `utils.py` completely rewritten — removed the large `DEFAULT_STYLE_CONFIG`
  element-level dict; replaced with `DEFAULT_SECTION_STYLES` (per-section-type classes)
- **BREAKING**: old `process_headings`, `process_markdown_section`,
  `apply_element_styling`, `process_block_content`, and `wrap_sections_odoo` functions
  removed from `utils.py` (a compatibility alias for `wrap_sections_odoo` is kept)
- `converter.py` rewritten to use the new section-detection pipeline
- HTML document now uses a lightweight self-contained CSS reset + grid (no Bootstrap CDN
  dependency) making it fully standalone and Odoo Apps Store sanitizer-safe
- Fixed image-path off-by-one bug: `static/description/` prefix (19 chars) is now
  correctly stripped instead of only 18 chars

### Removed
- `DEFAULT_STYLE_CONFIG` (replaced by `DEFAULT_SECTION_STYLES`)
- `process_headings`, `process_markdown_section`, `apply_element_styling`,
  `process_block_content` helper functions

## [0.6.0] - 2025-12-09

### Added
- Custom resource injection support via `--stylesheet` and `--script` CLI options
- Ability to inject custom CSS stylesheets into generated HTML
- Ability to inject custom JavaScript files into generated HTML
- Support for comma-separated lists of multiple stylesheets and scripts
- Enhanced Python API with `stylesheets` and `scripts` parameters in `convert_md_to_html()`
- Google Fonts integration (Inter font) for improved typography
- Card hover effects with smooth transitions for better user experience

### Changed
- Updated documentation in README.md with examples for custom resource injection
- Enhanced HTML template to support external stylesheet and script injection
- Improved meta tags for better SEO and viewport settings

### Improved
- Better flexibility for customization without modifying core styling
- Enhanced documentation with comprehensive examples for stylesheet and script injection
- More professional typography with Inter font family integration

## [0.5.0] - 2025-07-09

### Added
- Comprehensive Odoo frontend styling system using classes from web.assets_frontend.min.css
- Dictionary-based style configuration system for flexible customization
- Support for custom style configurations via JSON files
- New `--style-config` command-line option to load custom styling
- New `--show-config` option to display default styling configuration
- Enhanced semantic HTML5 element support
- Improved typography styling with Odoo-specific classes
- Better card and section layout system
- Enhanced table styling with striped and hover effects
- Improved form element styling
- Better responsive design with comprehensive CSS classes

### Changed
- **BREAKING**: Removed Bootstrap template system (modern, simple, odoo templates)
- **BREAKING**: Now uses only Odoo frontend styling by default
- Updated HTML output structure to use Odoo's oe_structure classes
- Improved image handling with better responsive classes
- Enhanced section wrapping logic for better content organization
- Updated CLI interface to focus on style configuration rather than templates
- Improved error handling and validation for style configurations

### Improved
- Better documentation with comprehensive examples
- More robust content processing with section preservation
- Enhanced image path handling and copying
- Better responsive design implementation
- Improved accessibility with semantic HTML structure

### Removed
- Bootstrap CDN dependencies
- Template selection system (--template option)
- Multiple template styles (modern, simple, odoo)

## [0.3.0] - 2025-04-21

### Added
- Multiple template styles: modern, simple, and Odoo-specific
- Bootstrap integration for responsive design
- New command-line option `--template` to select template style
- Bootstrap classes for all HTML elements
- Enhanced image handling with automatic responsiveness
- Improved handling of static/description paths for images

### Changed
- Updated default styling to be more compatible with Odoo Apps Store
- `wrap_sections` function now has a Bootstrap counterpart `wrap_sections_bootstrap`
- Updated image handling logic for better path resolution
- Updated the documentation to reflect new features

## [0.2.1] - 2024

### Fixed
- Image handling improvements
- Fixed path issues with Windows paths

## [0.2.0] - 2024

### Added
- Support for direct HTML sections in markdown files
- Automatic image handling and migration
- Custom output path options

## [0.1.0] - 2024

### Added
- Initial release
- Automatically converts Markdown to styled HTML
- Creates responsive card-based layouts for content
- Simple command-line interface