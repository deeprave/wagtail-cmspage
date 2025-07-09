
from cmspage.blocks.form import FormBlock
from cmspage.blocks.fields import (
    TextFieldBlock, EmailFieldBlock, IntegerFieldBlock, DecimalFieldBlock,
    SelectFieldBlock, MultiSelectFieldBlock, TextAreaFieldBlock
)


class TestFormFieldBlocks:
    """Test suite for form field blocks"""

    def test_form_block_structure(self):
        """Test FormBlock structure and fields"""
        block = FormBlock()

        # Check required fields
        assert "form_title" in block.child_blocks
        assert "form_description" in block.child_blocks
        assert "submit_url" in block.child_blocks
        assert "submit_button_text" in block.child_blocks
        assert "success_message" in block.child_blocks
        assert "fields" in block.child_blocks

    def test_text_field_block_exists(self):
        """Test TextFieldBlock can be instantiated"""
        block = TextFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_email_field_block_exists(self):
        """Test EmailFieldBlock can be instantiated"""
        block = EmailFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_integer_field_block_exists(self):
        """Test IntegerFieldBlock can be instantiated"""
        block = IntegerFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_decimal_field_block_exists(self):
        """Test DecimalFieldBlock can be instantiated"""
        block = DecimalFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_select_field_block_exists(self):
        """Test SelectFieldBlock can be instantiated"""
        block = SelectFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_multi_select_field_block_exists(self):
        """Test MultiSelectFieldBlock can be instantiated"""
        block = MultiSelectFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_textarea_field_block_exists(self):
        """Test TextAreaFieldBlock can be instantiated"""
        block = TextAreaFieldBlock()
        assert hasattr(block, "child_blocks")
        assert isinstance(block.child_blocks, dict)

    def test_form_block_default_values(self):
        """Test FormBlock default values"""
        block = FormBlock()

        # Get default value
        default_value = block.get_default()

        # Check that defaults exist
        assert default_value is not None

    def test_form_block_field_stream_structure(self):
        """Test FormBlock fields StreamBlock structure"""
        block = FormBlock()
        fields_block = block.child_blocks["fields"]

        # Check that the fields StreamBlock has the expected field types
        field_types = list(fields_block.child_blocks.keys())

        expected_types = [
            "text_field", "textarea_field", "email_field",
            "integer_field", "decimal_field", "select_field",
            "multiselect_field"
        ]

        for expected_type in expected_types:
            assert expected_type in field_types


class TestFormFieldBlocksBasic:
    """Basic validation tests for form field blocks"""

    def test_field_blocks_basic_validation(self):
        """Test basic validation for all field blocks"""
        blocks = [
            TextFieldBlock(),
            EmailFieldBlock(),
            IntegerFieldBlock(),
            DecimalFieldBlock(),
            SelectFieldBlock(),
            MultiSelectFieldBlock(),
            TextAreaFieldBlock()
        ]

        for block in blocks:
            # Each block should be able to handle empty values
            default_value = block.get_default()
            # Should not raise an error
            assert default_value is not None or block.required is False

    def test_form_block_to_python(self):
        """Test FormBlock to_python method"""
        block = FormBlock()

        test_data = {
            "form_title": "Test Form",
            "form_description": "A test form",
            "submit_url": "/submit/",
            "submit_button_text": "Submit",
            "success_message": "Success!",
            "fields": []
        }

        result = block.to_python(test_data)

        # Should return the data structure
        assert result["form_title"] == "Test Form"
        assert result["submit_url"] == "/submit/"
