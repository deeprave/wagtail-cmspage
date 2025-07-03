import pytest
from unittest.mock import Mock, patch
from django.template import Context, Template
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
