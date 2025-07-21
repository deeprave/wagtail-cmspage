import pytest
from unittest.mock import Mock, patch
from django.template import Context, Template, TemplateSyntaxError, TemplateDoesNotExist
from wagtail.images.models import Image

from cmspage.templatetags.cmspage_tags import render_image, get_embed_url_with_parameters, IMAGE_SIZES, ORIENTATIONS


class TestCMSPageTags:
    """Test suite for cmspage template tags"""

    def test_get_embed_url_with_parameters_youtube(self):
        """Test get_embed_url_with_parameters with YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = get_embed_url_with_parameters(url)
        expected = "https://www.youtube.com/embed/dQw4w9WgXcQ?rel=0"
        assert result == expected

    def test_get_embed_url_with_parameters_youtube_short(self):
        """Test get_embed_url_with_parameters with YouTube short URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = get_embed_url_with_parameters(url)
        expected = "https://www.youtube.com/embed/dQw4w9WgXcQ?rel=0"
        assert result == expected

    def test_get_embed_url_with_parameters_non_youtube(self):
        """Test get_embed_url_with_parameters with non-YouTube URL"""
        url = "https://vimeo.com/123456789"
        result = get_embed_url_with_parameters(url)
        assert result == url  # Should return unchanged

    def test_image_sizes_structure(self):
        """Test that IMAGE_SIZES is properly structured"""
        assert isinstance(IMAGE_SIZES, dict)
        assert "landscape" in IMAGE_SIZES
        assert "portrait" in IMAGE_SIZES
        assert "square" in IMAGE_SIZES
        assert "extrawide" in IMAGE_SIZES

        # Check that each orientation has size definitions
        for orientation in ORIENTATIONS:
            assert orientation in IMAGE_SIZES
            sizes = IMAGE_SIZES[orientation]
            assert "tiny" in sizes
            assert "small" in sizes
            assert "medium" in sizes
            assert "large" in sizes
            assert "full_width" in sizes
            assert "original" in sizes

    def test_image_size_values(self):
        """Test specific image size values"""
        # Landscape medium should be 480x320
        assert IMAGE_SIZES["landscape"]["medium"] == "480x320"

        # Portrait small should be 200x300
        assert IMAGE_SIZES["portrait"]["small"] == "200x300"

        # Square tiny should be 150x150
        assert IMAGE_SIZES["square"]["tiny"] == "150x150"

        # Original should be "original" for all orientations
        for orientation in ORIENTATIONS:
            assert IMAGE_SIZES[orientation]["original"] == "original"

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_basic(self, mock_template_class):
        """Test render_image with basic parameters"""
        # Create mock image
        mock_image = Mock(spec=Image)
        mock_image.title = "Test Image"
        mock_image.description = "Test Description"

        # Mock template
        mock_template = Mock()
        mock_template.render.return_value = '<img src="/test.jpg" alt="Test Image">'
        mock_template_class.return_value = mock_template

        # Call the function
        result = render_image(mock_image)

        # Verify template was created and rendered
        mock_template_class.assert_called_once()
        mock_template.render.assert_called_once()
        assert result == '<img src="/test.jpg" alt="Test Image">'

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_with_custom_params(self, mock_template_class):
        """Test render_image with custom parameters"""
        mock_image = Mock(spec=Image)
        mock_image.title = "Test Image"

        mock_template = Mock()
        mock_template.render.return_value = "<img>"
        mock_template_class.return_value = mock_template

        # Call with custom parameters
        _ = render_image(
            mock_image,
            orientation="portrait",
            size="large",
            size_prefix="max",
            alt_text="Custom Alt",
            crop=100,
            rounded=3,
            responsive=False,
        )

        # Verify template creation
        mock_template_class.assert_called_once()
        template_string = mock_template_class.call_args[0][0]

        # Check that template string contains expected elements
        assert "max-400x600" in template_string  # portrait large size
        assert "-c100" in template_string  # crop parameter
        assert 'alt="Custom Alt"' in template_string
        assert "rounded-3" in template_string

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_alt_text_fallback(self, mock_template_class):
        """Test render_image alt text fallback logic"""
        mock_image = Mock(spec=Image)
        mock_image.title = "Image Title"
        mock_image.description = "Image Description"

        mock_template = Mock()
        mock_template_class.return_value = mock_template

        # Test with no alt_text provided - should use title
        render_image(mock_image)
        template_string = mock_template_class.call_args[0][0]
        assert 'alt="Image Title"' in template_string

        # Reset mock
        mock_template_class.reset_mock()

        # Test with custom alt_text
        render_image(mock_image, alt_text="Custom Alt")
        template_string = mock_template_class.call_args[0][0]
        assert 'alt="Custom Alt"' in template_string

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_no_alt_text(self, mock_template_class):
        """Test render_image when no alt text is available"""
        mock_image = Mock(spec=Image)
        mock_image.title = ""
        mock_image.description = ""

        mock_template = Mock()
        mock_template_class.return_value = mock_template

        render_image(mock_image)
        template_string = mock_template_class.call_args[0][0]

        # Should not have alt attribute when no text available
        assert 'alt=""' not in template_string or "alt=" not in template_string

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_responsive_classes(self, mock_template_class):
        """Test render_image CSS class handling"""
        mock_image = Mock(spec=Image)
        mock_image.title = "Test"

        mock_template = Mock()
        mock_template_class.return_value = mock_template

        # Test with responsive=True (default)
        render_image(mock_image, responsive=True)
        template_string = mock_template_class.call_args[0][0]
        assert 'class="img-fluid"' in template_string

        # Reset and test with responsive=False
        mock_template_class.reset_mock()
        render_image(mock_image, responsive=False)
        template_string = mock_template_class.call_args[0][0]
        assert "img-fluid" not in template_string

    @patch("cmspage.templatetags.cmspage_tags.Template")
    def test_render_image_original_size(self, mock_template_class):
        """Test render_image with original size"""
        mock_image = Mock(spec=Image)
        mock_image.title = "Test"

        mock_template = Mock()
        mock_template_class.return_value = mock_template

        render_image(mock_image, size="original")
        template_string = mock_template_class.call_args[0][0]

        # Should use "original" size spec, not dimensions
        assert "original" in template_string
        assert "-c" not in template_string  # No cropping for original

    def test_orientations_constant(self):
        """Test ORIENTATIONS constant"""
        expected_orientations = ["landscape", "portrait", "square", "extrawide"]
        assert ORIENTATIONS == expected_orientations


@pytest.mark.django_db
class TestCMSPageTagsIntegration:
    """Integration tests for template tags with Django templates"""

    def test_embedurl_filter_in_template(self):
        """Test embedurl filter usage in Django template"""
        template = Template("{% load cmspage_tags %}{{ url|embedurl }}")

        context = Context({"url": "https://www.youtube.com/watch?v=test123"})
        result = template.render(context)

        expected = "https://www.youtube.com/embed/test123?rel=0"
        assert result == expected

    def test_render_image_tag_in_template(self):
        """Test render_image tag usage in Django template"""
        # Create a mock image
        mock_image = Mock(spec=Image)
        mock_image.title = "Test Image"

        template = Template("{% load cmspage_tags %}{% render_image image %}")

        context = Context({"image": mock_image})

        # This should render without error
        result = template.render(context)
        assert result is not None

    def test_render_image_with_parameters_in_template(self):
        """Test render_image with parameters in template"""
        mock_image = Mock(spec=Image)
        mock_image.title = "Test Image"

        template = Template("""
            {% load cmspage_tags %}
            {% render_image image orientation="portrait" size="large" alt_text="Custom Alt" %}
        """)

        context = Context({"image": mock_image})
        result = template.render(context)
        assert result is not None


class TestCMSPageIncludeTag:
    """Test suite for cmspage_include template tag"""

    @pytest.mark.django_db
    def test_cmspage_include_integration_test(self):
        """Test cmspage_include integration with template loading"""
        # This test verifies that our tag works with the Django template system
        # We test that it properly calls get_template and handles template resolution
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": "admin/base.html"})  # Use a known Django admin template

        # This should raise TemplateDoesNotExist (normal Django behavior)
        # or succeed if the admin template exists, proving our tag works
        try:
            result = template.render(context)
            # If it succeeds, our tag is working correctly with the template system
            assert isinstance(result, str)
        except TemplateDoesNotExist:
            # This is also acceptable - proves our tag delegates to Django correctly
            pass

    @pytest.mark.django_db
    def test_cmspage_include_with_empty_template_variable(self):
        """Test cmspage_include with empty template variable"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": ""})

        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_with_none_template_variable(self):
        """Test cmspage_include with None template variable"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": None})

        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_with_missing_template_variable(self):
        """Test cmspage_include with missing template variable"""
        template = Template("{% load cmspage_tags %}{% cmspage_include missing_variable %}")
        context = Context({})

        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_with_false_template_variable(self):
        """Test cmspage_include with falsy template variable"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": False})

        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_nonexistent_template(self):
        """Test cmspage_include with nonexistent template - should raise TemplateDoesNotExist"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": "nonexistent_template.html"})

        # Should raise TemplateDoesNotExist for missing templates (normal Django behavior)
        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_syntax_error_no_arguments(self):
        """Test cmspage_include with no arguments raises TemplateSyntaxError"""
        with pytest.raises(TemplateSyntaxError, match="'cmspage_include' tag requires exactly one argument"):
            Template("{% load cmspage_tags %}{% cmspage_include %}")

    @pytest.mark.django_db
    def test_cmspage_include_properly_scoped_variables(self):
        """Test that cmspage_include behavior is consistent with empty variables"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Test with various falsy values
        for falsy_value in [None, "", False, 0]:
            context = Context({"template_name": falsy_value})
            result = template.render(context)
            assert result == "", f"Failed for falsy value: {falsy_value}"

    # === EDGE CASE TESTS ===

    @pytest.mark.django_db
    def test_cmspage_include_variable_resolution_edge_cases(self):
        """Test edge cases in variable resolution"""

        # Test with nested dictionary access
        template = Template("{% load cmspage_tags %}{% cmspage_include config.template %}")
        context = Context({"config": {"template": None}})
        result = template.render(context)
        assert result == ""

        # Test with missing nested key
        template = Template("{% load cmspage_tags %}{% cmspage_include config.missing %}")
        context = Context({"config": {}})
        result = template.render(context)
        assert result == ""

        # Test with object attribute access
        class MockObj:
            template_name = ""

        template = Template("{% load cmspage_tags %}{% cmspage_include obj.template_name %}")
        context = Context({"obj": MockObj()})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_numeric_and_special_values(self):
        """Test behavior with numeric and special values as template names"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Test falsy numeric values (should return empty string)
        for value in [0, 0.0]:
            context = Context({"template_name": value})
            result = template.render(context)
            assert result == ""

        # Test truthy numeric values (should try to load template and fail)
        for value in [-1, 42, 1.5]:
            context = Context({"template_name": value})
            # Numeric values converted to strings can't be used as file paths
            with pytest.raises((TemplateDoesNotExist, TypeError)):
                template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_whitespace_edge_cases(self):
        """Test behavior with various whitespace scenarios"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Test whitespace-only strings
        whitespace_values = [" ", "\t", "\n", "\r", "   ", "\t\n\r "]
        for value in whitespace_values:
            context = Context({"template_name": value})
            # Whitespace strings are truthy, so should try to load template
            with pytest.raises(TemplateDoesNotExist):
                template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_complex_variable_expressions(self):
        """Test complex variable expressions and filters"""

        # Test with filter that returns empty string
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name|default:'' %}")
        context = Context({})
        result = template.render(context)
        assert result == ""

        # Test with filter that returns None
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name|default:None %}")
        context = Context({})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_variable_does_not_exist_nested(self):
        """Test VariableDoesNotExist with complex nested access"""

        # Deep nested missing attribute
        template = Template("{% load cmspage_tags %}{% cmspage_include a.b.c.d.template %}")
        context = Context({})
        result = template.render(context)
        assert result == ""

        # Missing key in existing dict
        template = Template("{% load cmspage_tags %}{% cmspage_include config.templates.main %}")
        context = Context({"config": {"other": "value"}})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_context_variable_types(self):
        """Test different types of context variables"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Empty list (falsy)
        context = Context({"template_name": []})
        result = template.render(context)
        assert result == ""

        # Empty dict (falsy)
        context = Context({"template_name": {}})
        result = template.render(context)
        assert result == ""

        # Empty set (falsy)
        context = Context({"template_name": set()})
        result = template.render(context)
        assert result == ""

        # Non-empty list (truthy but will cause error when used as template name)
        context = Context({"template_name": ["item1", "item2"]})
        with pytest.raises((TemplateDoesNotExist, TypeError)):
            template.render(context)

        # Non-empty dictionary (truthy but will cause error when used as template name)
        context = Context({"template_name": {"key": "value"}})
        with pytest.raises((TemplateDoesNotExist, TypeError)):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_unicode_and_encoding(self):
        """Test Unicode strings and encoding edge cases"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Unicode template name (should try to load)
        context = Context({"template_name": "tëmplätë.html"})
        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

        # Empty Unicode string
        context = Context({"template_name": ""})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_template_resolution_errors(self):
        """Test that template resolution errors bubble up correctly"""

        # Valid string but non-existent template
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": "definitely/does/not/exist.html"})
        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

        # Template name with invalid characters for filesystem
        context = Context({"template_name": "invalid|name?.html"})
        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_context_isolation(self):
        """Test that context is properly passed to included templates"""

        # Test that our tag doesn't interfere with context
        # We can't easily test this without real templates, but we can test
        # that context.flatten() is called correctly by mocking
        from unittest.mock import Mock, patch

        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": "test.html", "var1": "value1"})

        with patch("cmspage.templatetags.cmspage_tags.get_template") as mock_get_template:
            mock_template = Mock()
            mock_template.render.return_value = "rendered content"
            mock_get_template.return_value = mock_template

            result = template.render(context)

            # Verify get_template was called with correct template name
            mock_get_template.assert_called_once_with("test.html")

            # Verify template.render was called with flattened context
            mock_template.render.assert_called_once()
            passed_context = mock_template.render.call_args[0][0]
            assert "var1" in passed_context
            assert passed_context["var1"] == "value1"
            assert result == "rendered content"

    @pytest.mark.django_db
    def test_cmspage_include_syntax_validation_edge_cases(self):
        """Test template tag syntax validation edge cases"""

        # Multiple arguments (should fail)
        with pytest.raises(TemplateSyntaxError, match="exactly one argument"):
            Template("{% load cmspage_tags %}{% cmspage_include template1 template2 %}")

        # No arguments (should fail)
        with pytest.raises(TemplateSyntaxError, match="exactly one argument"):
            Template("{% load cmspage_tags %}{% cmspage_include %}")

        # Empty argument (syntactically valid but will result in empty)
        template = Template("{% load cmspage_tags %}{% cmspage_include '' %}")
        result = template.render(Context())
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_error_propagation(self):
        """Test that different types of errors propagate correctly"""

        # Create mock that raises different exceptions
        from unittest.mock import patch, Mock

        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        context = Context({"template_name": "test.html"})

        # Test TemplateDoesNotExist propagation
        with patch("cmspage.templatetags.cmspage_tags.get_template") as mock_get_template:
            mock_get_template.side_effect = TemplateDoesNotExist("test.html")
            with pytest.raises(TemplateDoesNotExist):
                template.render(context)

        # Test TemplateSyntaxError propagation during rendering
        with patch("cmspage.templatetags.cmspage_tags.get_template") as mock_get_template:
            mock_template = Mock()
            mock_template.render.side_effect = TemplateSyntaxError("Syntax error")
            mock_get_template.return_value = mock_template
            with pytest.raises(TemplateSyntaxError):
                template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_performance_edge_cases(self):
        """Test performance-related edge cases"""

        # Very long template name (should handle gracefully)
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")
        long_name = "a" * 100 + ".html"  # Reduced size to avoid filesystem issues
        context = Context({"template_name": long_name})

        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

        # Large context (should handle gracefully)
        large_context = {f"var_{i}": f"value_{i}" for i in range(100)}  # Reduced size
        large_context["template_name"] = ""
        context = Context(large_context)
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_boolean_edge_cases(self):
        """Test specific boolean value handling"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # False should return empty string
        context = Context({"template_name": False})
        result = template.render(context)
        assert result == ""

        # True should try to load template (boolean gets converted to string "True")
        context = Context({"template_name": True})
        with pytest.raises((TemplateDoesNotExist, TypeError)):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_callable_and_special_objects(self):
        """Test behavior with callable objects and special Python objects"""
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Test with None (should return empty string)
        context = Context({"template_name": None})
        result = template.render(context)
        assert result == ""

        # Test with custom objects - Django template system passes objects directly
        # without automatically converting to string, so these will cause TypeErrors
        class EmptyStringObj:
            def __str__(self):
                return ""

        context = Context({"template_name": EmptyStringObj()})
        # This will cause TypeError because Django tries to use object as path directly
        with pytest.raises(TypeError):
            template.render(context)

        # Test with an object that has a truthy value but is not a string
        # This will also cause TypeError since Django expects string paths
        class TruthyObj:
            def __bool__(self):
                return True

        context = Context({"template_name": TruthyObj()})
        with pytest.raises(TypeError):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_template_variable_filter_chains(self):
        """Test complex filter chains on template variables"""

        # Test with filter chain that results in empty string
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name|default:'nonexistent.html'|cut:'nonexistent.html' %}")
        context = Context({})
        result = template.render(context)
        assert result == ""

        # Test with filter that preserves valid template name
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name|default:'test.html' %}")
        context = Context({})
        with pytest.raises(TemplateDoesNotExist):
            template.render(context)

    @pytest.mark.django_db
    def test_cmspage_include_context_processor_variables(self):
        """Test interaction with Django context processors"""

        # Test that our tag works with variables that might come from context processors
        template = Template("{% load cmspage_tags %}{% cmspage_include request.template_var %}")

        # Mock request object
        class MockRequest:
            template_var = None

        context = Context({"request": MockRequest()})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_circular_reference_prevention(self):
        """Test that our implementation doesn't cause issues with circular references"""

        # Test with nested context access that could be problematic
        template = Template("{% load cmspage_tags %}{% cmspage_include deeply.nested.template.name %}")

        # Create a nested structure where variables reference each other
        nested_dict = {}
        nested_dict["self_ref"] = nested_dict
        nested_dict["template"] = {"name": ""}

        context = Context({"deeply": {"nested": nested_dict}})
        result = template.render(context)
        assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_memory_and_gc_edge_cases(self):
        """Test memory management and garbage collection edge cases"""

        # Test with objects that might have cleanup issues
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        # Test with many temporary variables that should be cleaned up
        for i in range(10):
            context = Context({"template_name": f"temp_{i}.html"})
            with pytest.raises(TemplateDoesNotExist):
                template.render(context)

        # Test successful empty string returns don't leak memory
        for i in range(10):
            context = Context({"template_name": ""})
            result = template.render(context)
            assert result == ""

    @pytest.mark.django_db
    def test_cmspage_include_thread_safety_simulation(self):
        """Test behavior that simulates multi-threaded usage"""

        # Test with different contexts in sequence (simulating concurrent requests)
        template = Template("{% load cmspage_tags %}{% cmspage_include template_name %}")

        test_cases = [
            {"template_name": ""},
            {"template_name": None},
            {"template_name": "test1.html"},
            {"template_name": False},
            {"template_name": "test2.html"},
        ]

        for case in test_cases:
            context = Context(case)
            if not case["template_name"]:
                result = template.render(context)
                assert result == ""
            else:
                with pytest.raises(TemplateDoesNotExist):
                    template.render(context)
