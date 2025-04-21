# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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