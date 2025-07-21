# Development TODO List

## Form Validation System Implementation

### Critical Issues - Form Block Validation

The current form block system lacks proper backend validation and processing. Forms can accept user input but cannot properly validate or process submissions.

### Required Components

#### 1. Field-Level Validation Framework
- **Field Validation Hooks**: Each field block type needs to provide validation methods similar to Django's field validation
  - `TextFieldBlock` → equivalent to Django `CharField` validation
  - `EmailFieldBlock` → equivalent to Django `EmailField` validation
  - `IntegerFieldBlock` → equivalent to Django `IntegerField` validation
  - `DecimalFieldBlock` → equivalent to Django `DecimalField` validation
  - `SelectFieldBlock` → choice validation with option checking
  - `MultiSelectFieldBlock` → multiple choice validation

- **Field Validator Interface**: Each field block should implement:
  ```python
  def clean(self, value):
      """Clean and validate field value, raise ValidationError if invalid"""
      pass

  def get_form_field(self):
      """Return equivalent Django form field for this block"""
      pass
  ```

#### 2. Form-Level Validation System
- **Form Validator**: `FormBlock` should implement validation that mirrors Django's form validation:
  ```python
  def clean(self, form_data):
      """Validate entire form, cross-field validation"""
      pass

  def is_valid(self, form_data):
      """Run all field and form validators"""
      pass
  ```

- **Integration with Django Forms**: Consider creating a bridge between StreamField blocks and Django forms for consistent validation patterns

#### 3. Server-Side Processing
- **Form Submission Handler**: Create view(s) to handle form submissions from `submit_url`
  - Validate CSRF tokens
  - Run field-level validation
  - Run form-level validation
  - Process valid submissions
  - Return appropriate JSON responses for AJAX

- **Error Handling**: Proper error messages that map back to specific fields in the frontend

#### 4. Security Enhancements
- **Input Sanitization**: All user input must be properly sanitized
- **URL Validation**: `submit_url` should be validated against allowed patterns
- **Rate Limiting**: Consider adding rate limiting for form submissions

### Implementation Priority
1. **High**: Field validation hooks and basic server-side validation
2. **High**: Form submission handler with proper error responses
3. **Medium**: Django forms integration for consistency
4. **Medium**: Enhanced security measures

### Notes
- Follow Django's validation patterns for consistency with the ecosystem
- Ensure backward compatibility with existing form blocks
- Consider performance implications of validation for large forms
- Document validation patterns for developers extending the system

### Related Files
- `cmspage/blocks/form.py` - Main form block definition
- `cmspage/blocks/fields/` - All field block definitions
- `cmspage/templates/blocks/form_block.html` - Frontend form template
- `tests/test_blocks_form.py` - Current limited tests
