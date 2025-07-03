import pytest
from unittest.mock import Mock, patch
from django.template import TemplateDoesNotExist
from django.test import RequestFactory

from cmspage.mixins import CMSTemplateMixin


class TestCMSTemplateMixin:
    """Test suite for CMSTemplateMixin functionality"""

    @pytest.fixture
    def mixin_instance(self):
        """Create a test instance with CMSTemplateMixin"""
        class TestClass(CMSTemplateMixin):
            pk = 1
            __module__ = "tests.test_mixins"

        return TestClass()

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    def test_template_styles_single_string(self, mixin_instance, settings):
        """Test template_styles property with single string configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = "bootstrap5"
        result = mixin_instance.template_styles
        assert result == ["bootstrap5"]

    def test_template_styles_comma_separated(self, mixin_instance, settings):
        """Test template_styles property with comma-separated configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = "bootstrap5,tailwind"
        result = mixin_instance.template_styles
        assert result == ["bootstrap5", "tailwind"]

    def test_template_styles_space_separated(self, mixin_instance, settings):
        """Test template_styles property with space-separated configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = "bootstrap5 tailwind"
        result = mixin_instance.template_styles
        assert result == ["bootstrap5", "tailwind"]

    def test_template_styles_list(self, mixin_instance, settings):
        """Test template_styles property with list configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = ["bootstrap5", "tailwind"]
        result = mixin_instance.template_styles
        assert result == ["bootstrap5", "tailwind"]

    def test_template_styles_none(self, mixin_instance, settings):
        """Test template_styles property with None configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = None
        result = mixin_instance.template_styles
        assert result == []

    def test_template_styles_empty_string(self, mixin_instance, settings):
        """Test template_styles property with empty string configuration"""
        settings.CMSPAGE_TEMPLATE_STYLES = ""
        result = mixin_instance.template_styles
        # Empty string becomes [''] due to split behavior
        assert result == [""]

    def test_include_names_default(self, mixin_instance, settings):
        """Test include_names property with default configuration"""
        if hasattr(settings, "CMSPAGE_TEMPLATE_INCLUDE_FILES"):
            delattr(settings, "CMSPAGE_TEMPLATE_INCLUDE_FILES")
        result = mixin_instance.include_names
        expected = [
            "title", "header", "logo", "navigation", "navigation_item",
            "navigation_top", "navigation_top_item", "navigation_side",
            "navigation_side_item", "messages", "logo", "carousel", "main",
            "footer", "links", "contact", "media"
        ]
        assert result == expected

    def test_include_names_custom_string(self, mixin_instance, settings):
        """Test include_names property with custom string configuration"""
        settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = "header,footer,main"
        result = mixin_instance.include_names
        assert result == ["header", "footer", "main"]

    def test_include_names_custom_list(self, mixin_instance, settings):
        """Test include_names property with custom list configuration"""
        settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = ["header", "footer", "main"]
        result = mixin_instance.include_names
        assert result == ["header", "footer", "main"]

    def test_base_template_with_absolute_path(self, mixin_instance, settings):
        """Test base_template property with absolute path"""
        settings.CMSPAGE_TEMPLATE_BASE = "/absolute/path/base.html"
        result = mixin_instance.base_template
        assert result == "absolute/path/base.html"

    def test_base_template_with_relative_path(self, mixin_instance, settings):
        """Test base_template property with relative path"""
        settings.CMSPAGE_TEMPLATE_BASE = "base.html"
        settings.CMSPAGE_TEMPLATE_BASE_DIR = "custom"
        result = mixin_instance.base_template
        assert result == "custom/base.html"

    @patch("django.template.engines")
    def test_find_existing_template_found(self, mock_engines, mixin_instance):
        """Test find_existing_template when template is found"""
        mock_engine = Mock()
        mock_engine.engine.find_template.return_value = Mock()
        mock_engines.all.return_value = [mock_engine]

        result = mixin_instance.find_existing_template("cmspage/bootstrap5/test.html")
        assert result == "cmspage/bootstrap5/test.html"

    @patch("django.template.engines")
    def test_find_existing_template_not_found(self, mock_engines, mixin_instance):
        """Test find_existing_template when no template is found"""
        mock_engine = Mock()
        mock_engine.engine.find_template.side_effect = TemplateDoesNotExist("Not found")
        mock_engines.all.return_value = [mock_engine]

        result = mixin_instance.find_existing_template("cmspage/nonexistent.html")
        # Returns original path as fallback when not found
        assert result == "cmspage/nonexistent.html"

    def test_include_templates_basic(self, mixin_instance, settings):
        """Test basic include_templates functionality"""
        settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = "header,footer"

        # Just verify the property exists and is callable/accessible
        assert hasattr(mixin_instance, "include_templates")


@pytest.mark.django_db
class TestCMSTemplateMixinIntegration:
    """Integration tests for CMSTemplateMixin with Django components"""

    def test_template_resolution_with_django_loader(self, settings, rf):
        """Test actual template resolution with Django's template loader"""
        from cmspage.models import CMSPage

        settings.CMSPAGE_TEMPLATE_STYLES = None
        page = CMSPage(title="Test Page")
        page.pk = 1

        # get_template requires a request parameter
        request = rf.get("/")
        template_path = page.get_template(request)
        assert template_path == "cmspage/cms_page.html"

    def test_context_building(self, settings, rf):
        """Test context building with all components"""
        from cmspage.models import CMSPage

        settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = "header,footer"
        page = CMSPage(title="Test Page")
        page.pk = 1

        request = rf.get("/")
        context = page.get_context(request)

        assert "base_template" in context
        assert "include" in context
        assert isinstance(context["include"], dict)
