import pytest
from unittest.mock import patch
from wagtail.images.models import Image

from cmspage.models.image import CMSPageImage


@pytest.mark.django_db
class TestCMSPageImage:
    """Test suite for CMSPageImage model"""

    def test_inheritance_from_wagtail_image(self):
        """Test that CMSPageImage properly inherits from Wagtail Image"""
        assert issubclass(CMSPageImage, Image)

    def test_cms_image_model_meta(self):
        """Test CMSPageImage model meta information"""
        assert CMSPageImage._meta.app_label == "cmspage"

    def test_save_method_exists(self):
        """Test that save method exists and can be called"""
        image = CMSPageImage(title="Test Image")
        # Test that save method exists
        assert hasattr(image, "save")
        assert callable(image.save)

    def test_webp_conversion_check(self):
        """Test WebP file name checking logic"""
        image = CMSPageImage(title="Test Image")

        # Mock a file name
        from unittest.mock import Mock
        mock_file = Mock()
        mock_file.name = "test.webp"
        image.file = mock_file

        # The save method should handle WebP files differently
        with patch.object(CMSPageImage.__bases__[0], "save") as mock_super_save:
            image.save()
            # Should call super().save() for WebP files
            mock_super_save.assert_called_once()

    def test_no_file_handling(self):
        """Test handling when no file is present"""
        image = CMSPageImage(title="No File Image")
        image.file = None

        with patch.object(CMSPageImage.__bases__[0], "save") as mock_super_save:
            image.save()
            # Should call super().save() when no file
            mock_super_save.assert_called_once()

    @patch("cmspage.models.image.WillowImage.open")
    @patch("cmspage.models.image.os.remove")
    @patch("builtins.open")
    def test_conversion_error_handling(self, mock_open, mock_remove, mock_willow):
        """Test error handling during conversion"""
        image = CMSPageImage(title="Error Test")

        # Mock a non-WebP file
        from unittest.mock import Mock
        mock_file = Mock()
        mock_file.name = "test.jpg"
        mock_file.path = "/fake/path/test.jpg"
        image.file = mock_file

        # Mock WillowImage.open to raise an exception
        mock_willow.side_effect = Exception("Conversion error")

        with patch.object(CMSPageImage.__bases__[0], "save") as mock_super_save:
            # Should handle the error gracefully and still call save
            image.save()
            mock_super_save.assert_called()


@pytest.mark.django_db
class TestCMSPageImageIntegration:
    """Integration tests for CMSPageImage"""

    def test_model_registration(self):
        """Test that the model is properly registered"""
        # Test that we can access the model through Django's app registry
        from django.apps import apps
        model = apps.get_model("cmspage", "CMSPageImage")
        assert model == CMSPageImage

    def test_wagtail_features_available(self):
        """Test that Wagtail image features are available"""
        image = CMSPageImage(title="Test")

        # Test that key Wagtail methods exist
        assert hasattr(image, "get_rendition")
        assert hasattr(image, "get_willow_image")
