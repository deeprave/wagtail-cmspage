## ChangeLog

### 2025.7.5

#### Added

* New `cmspage_include` template tag for safe template inclusion:
  * Gracefully handles empty, blank, or None template variables
  * Renders nothing instead of throwing errors when template path is empty
  * Delegates to Django's built-in `include` tag for full compatibility
  * Usage: `{% load cmspage_tags %}{% cmspage_include template_var %}`
  * Supports all include tag features: `with`, `only`, context variables
* Self-contained theme switcher component:
  * Added `theme_switcher` to default template includes
  * Provides light/dark/auto theme switching with localStorage persistence
  * Embedded JavaScript for zero external dependencies
  * Fully accessible with ARIA labels and keyboard navigation
  * Configurable via context variables:
    * `theme_switcher_enabled`: Enable/disable the switcher (default: True)
    * `theme_switcher_position`: Customize position with top/right values
    * `theme_switcher_icons`: Custom icon classes for light/auto/dark modes
  * Usage: `{% include include.theme_switcher %}` for CMS pages
  * Fallback: `{% include "cmspage/includes/theme_switcher.html" %}` for non-CMS pages

#### Changed

* Moved theme switcher styles from projects to wagtail-cmspage SCSS
* Theme switcher now included as standard component in wagtail-cmspage
* Completely revamped README.md with modern formatting, feature overview, and clear installation guide
* Updated documentation with CSS Styling & Bootstrap Integration section
* Enhanced CMSPAGE.md with comprehensive Bootstrap 5 integration guide
* Added comprehensive Content Editor Guide for non-technical users

### 2025.7.4

#### Changed

* **BREAKING**: Removed obsolete `Backgrounds` enum - replaced with new semantic `Palette` enum
* Updated `Palette` enum with Bootstrap-independent semantic color classes using `cp-*` prefix:
  * `NONE` → `cp-transparent` (transparent background)
  * `PAGE` → `cp-page` (respects light/dark mode)
  * `LIGHT` → `cp-light` (fixed light theme)
  * `DARK` → `cp-dark` (fixed dark theme)
  * `WHITE` → `cp-white` (black on white)
  * `BLACK` → `cp-black` (white on black)
  * `HIGHLIGHT` → `cp-highlight` (highlight theme)
  * `STANDOUT` → `cp-standout` (standout theme)
  * `SUCCESS` → `cp-success` (success/positive)
  * `WARNING` → `cp-warning` (warning/caution)
  * `INFO` → `cp-info` (informational)
  * `DANGER` → `cp-danger` (error/critical)
* Enhanced `Insets` enum with responsive padding classes (e.g., `p-1 p-sm-2`)
* Added CSS utilities for new color palette system in `cmspage/scss/partials/_utilities.scss`

#### Added

* Created data migration `palette_migration.py` to convert existing palette values
* Added comprehensive SQL migration queries and documentation in `PALETTE_MAPPING_LOG.md`
* New migration `0006_remove_backgrounds_enum.py` documenting enum removal

#### Technical

* New color palette system uses CSS custom properties for theme switching
* Bootstrap-independent design allows for better theme customization
* Responsive padding utilities improve mobile/desktop layout consistency
* Removed old theme toggle from base header template

### 2024.3.0

#### Added

* Created new `CMSFormPage` class for dynamic form handling
* Added form block functionality with nested sfields
* Implemented various form field block types:
  * `TextFieldBlock`: Standard text input field
  * `TextAreaFieldBlock`: Multi-line text input field
  * `EmailFieldBlock`: Email input field with validation
  * `IntegerFieldBlock`: Integer input field with min/max validation
  * `DecimalFieldBlock`: Decimal input field with precision control
  * `SelectFieldBlock`: Dropdown selection with configurable options
  * `MultiSelectFieldBlock`: Multiple selection field with configurable options
  * `OptionBlock`: Helper block for defining select options
* Created `FormBlock` container with form metadata (title, description, submit URL, etc.)
* Added Bootstrap compatible templates for form rendering:
  * Main form container template (`blocks/form_block.html`)
  * Field-specific templates for each input type
  * Client-side validation with feedback messages
  * AJAX form submission handling
  * Success message display
* Limited form blocks to one per page through StreamField configuration

#### Changed

* Extended base `CMSPageBase` functionality to support form capabilities
* Enhanced form field validation with appropriate constraints based on field type

#### Technical

* Added proper Django templates in the template directory structure
* Implemented Bootstrap 5 styling for all form elements
* Added client-side form validation and submission handling via JavaScript

### 2024.3.2

- Expanded CMSPage documentation with detailed installation, usage, and configuration instructions.
- Introduced CMSPageBase as an abstract base class for extending CMSPage functionality.
- Enhanced MenuLink model to support hierarchical menu structures and added caching capabilities.
- Removed Event model and related functionality, moved to related app.
- Updated context processors to reflect changes in navigation and site variables.
- Improved/enhanced template handling with support for multiple CSS frameworks and customizable template paths.
- Added new migration to alter MenuLink model fields.
- Updated pre-commit configuration and added new tests for context processors and template mixins.

#### BACKWARDS INCOMPATIBILTY

- Removed `Event` model and related functionality, moved to a related app.
- To avoid confuction about inherited templates, the "base" template name is now `cmspage/cmspage.html` instead of
  `cmspage/base.html`. This is to avoid confusion with the `base.html` template that is typically used by most
  Django/Wagtail projects.

### 2024.3.1

- Refactored the event model to consolidate date and time fields into a single DateTimeField.
- Improved naming consistency across models and methods, switched to more precise ordering and filtering in
  SnippetViewSet
- Removed unused form overrides, apparently not required.
- Bumped project's version number to 2024.3.1.

## 2024.3.0

- Add conditional caching
- Add context processor tests
  Move caching strategy to models to simplify context_processors
- Combined context processors for navigation, events and site variables into a single processor

## 2024.2.0

- Almost a complete rewrite, including:
  - moving template path generation to a separate possibly reusable mixin
  - support tiered template paths overridable via config for different frontend CSS frameworks
  - additional models/orderables for complex content structures
  - improved documentation
