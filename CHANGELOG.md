# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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