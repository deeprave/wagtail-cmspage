## ChangeLog


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
