## ChangeLog

### 2024.3.2

- Expanded CMSPage documentation with detailed installation, usage, and configuration instructions.
- Introduced CMSPageBase as an abstract base class for extending CMSPage functionality.
- Enhanced MenuLink model to support hierarchical menu structures and added caching capabilities.
- Removed Event model and related functionality, moved to related app.
- Updated context processors to reflect changes in navigation and site variables.
- Improved/enhanced template handling with support for multiple CSS frameworks and customizable template paths.
- Added new migration to alter MenuLink model fields.
- Updated pre-commit configuration and added new tests for context processors and template mixins.

### 2024.3.1

- Refactored the event model to consolidate date and time fields into a single DateTimeField.
- Improved naming consistency across models and methods, switched to more precise ordering and filtering in SnippetViewSet
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
