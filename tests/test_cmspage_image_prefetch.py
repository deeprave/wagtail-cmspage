from collections.abc import Mapping
from unittest.mock import MagicMock, patch

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from wagtail.images.models import Image as WagtailImage
from wagtail.images.tests.utils import get_test_image_file

from cmspage.models import CMSFooterPage, CMSPage, CMSPageImage


@pytest.mark.django_db
class TestCMSPageImagePrefetch:
    """Test suite for CMSPage image prefetching functionality"""

    def setup_method(self):
        """Set up test data for each test method"""
        # Create test images
        self.image1 = CMSPageImage.objects.create(
            title="Test Image 1",
            file=get_test_image_file(),
        )
        self.image2 = CMSPageImage.objects.create(
            title="Test Image 2",
            file=get_test_image_file(),
        )
        self.image3 = CMSPageImage.objects.create(
            title="Test Image 3",
            file=get_test_image_file(),
        )

    def test_extract_image_ids_from_cards_block(self):
        # sourcery skip: class-extract-method
        """Test extracting image IDs from a cards block"""
        # Create a mock cards block
        mock_block = MagicMock()
        mock_block.block_type = "cards"
        mock_block.value = {
            "cards": [
                {"image": self.image1},
                {"image": self.image2},
                {"text": "No image here"},
            ]
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert
        assert len(image_ids) == 2
        assert self.image1.id in image_ids
        assert self.image2.id in image_ids

    def test_extract_image_ids_from_carousel_block(self):
        """Test extracting image IDs from a carousel block"""
        # Create a mock carousel block
        mock_block = MagicMock()
        mock_block.block_type = "carousel"
        mock_block.value = {
            "carousel": [
                {"carousel_image": self.image1},
                {"carousel_image": self.image2},
                {"carousel_title": "No image here"},
            ]
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert
        assert len(image_ids) == 2
        assert self.image1.id in image_ids
        assert self.image2.id in image_ids

    def test_extract_image_ids_from_image_and_text_block(self):
        """Test extracting image IDs from an image_and_text block"""
        # Create a mock image_and_text block
        mock_block = MagicMock()
        mock_block.block_type = "image_and_text"
        mock_block.value = {
            "image": self.image1,
            "text": "Some text",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert
        assert len(image_ids) == 1
        assert self.image1.id in image_ids

    def test_extract_image_ids_from_large_image_block(self):
        """Test extracting image IDs from a large_image block"""
        # Create a mock large_image block
        mock_block = MagicMock()
        mock_block.block_type = "large_image"
        mock_block.value = {
            "image": self.image1,
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert
        assert len(image_ids) == 1
        assert self.image1.id in image_ids

    def test_extract_image_ids_from_generic_block(self):
        """Test extracting image IDs from a generic block with an image"""
        # Create a mock generic block
        mock_block = MagicMock()
        mock_block.block_type = "some_other_block"
        mock_block.value = {
            "image": self.image1,
            "text": "Some text",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert
        assert len(image_ids) == 1
        assert self.image1.id in image_ids

    def test_extract_image_ids_from_title_block(self):
        """Test extracting image IDs from a title block (which has no images)"""
        # Create a mock title block
        mock_block = MagicMock()
        mock_block.block_type = "title"
        mock_block.value = {
            "text": "This is a title",
            "cursive": False,
            "justify": "center",
            "palette": "warning",
            "inset": "small",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert that no image IDs were extracted
        assert len(image_ids) == 0

    def test_extract_image_ids_from_richtext_with_title_block(self):
        """Test extracting image IDs from a richtext_with_title block (which has no images)"""
        # Create a mock richtext_with_title block
        mock_block = MagicMock()
        mock_block.block_type = "richtext"
        mock_block.value = {
            "title": "This is a title",
            "cursive": False,
            "content": "<p>This is some rich text content</p>",
            "justify": "left",
            "palette": "warning",
            "inset": "small",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert that no image IDs were extracted
        assert len(image_ids) == 0

    def test_extract_image_ids_from_copyright_block(self):
        """Test extracting image IDs from a copyright block (which has no images)"""
        # Create a mock copyright block
        mock_block = MagicMock()
        mock_block.block_type = "copy"
        mock_block.value = {
            "copyright": "© 2025 Example Company",
            "palette": "warning",
            "inset": "small",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert that no image IDs were extracted
        assert len(image_ids) == 0

    def test_extract_image_ids_from_call_to_action_block(self):
        """Test extracting image IDs from a call_to_action block (which has no images)"""
        # Create a mock call_to_action block
        mock_block = MagicMock()
        mock_block.block_type = "cta"
        mock_block.value = {
            "title": "Call to Action",
            "cursive": False,
            "text": "<p>Click here to learn more</p>",
            "justify": "left",
            "palette": "warning",
            "inset": "small",
            "link": {"button_title": "Learn More", "page_link": None, "doc_link": None, "extra_link": "/learn-more"},
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert that no image IDs were extracted
        assert len(image_ids) == 0

    def test_extract_image_ids_from_new_section_block(self):
        """Test extracting image IDs from a new_section block (which has no images)"""
        # Create a mock new_section block
        mock_block = MagicMock()
        mock_block.block_type = "new_section"
        mock_block.value = {
            "height": "medium",
            "palette": "warning",
            "inset": "small",
        }

        # Call the method
        image_ids = CMSPage._extract_image_ids_from_block(mock_block)

        # Assert that no image IDs were extracted
        assert len(image_ids) == 0

    def test_iter_images_from_hero_streamfield_structvalue(self):
        page = CMSPage(title="Prefetch", body=[("hero", {"image": self.image1})])
        block = page.body[0]

        assert type(block.value).__name__ == "StructValue"
        assert isinstance(block.value, Mapping)

        images = list(CMSPage._iter_images_from_block(block))

        assert [image.id for image in images] == [self.image1.id]

    def test_iter_images_from_cards_streamfield_structvalue(self):
        page = CMSPage(
            title="Prefetch",
            body=[("cards", {"cards": [{"image": self.image1}, {"image": self.image2}]})],
        )

        images = list(CMSPage._iter_images_from_block(page.body[0]))

        assert [image.id for image in images] == [self.image1.id, self.image2.id]

    def test_iter_images_from_footer_streamfield_structvalue(self):
        footer = CMSFooterPage(title="Footer", footer=[("info", {"image": self.image3})])

        images = list(CMSPage._iter_images_from_block(footer.footer[0]))

        assert [image.id for image in images] == [self.image3.id]

    def _assert_get_rendition_skips_cache_and_sql(self, image, spec):
        rendition_model = image.get_rendition_model()
        with patch.object(rendition_model.cache_backend, "get_many") as get_many:
            with CaptureQueriesContext(connection) as ctx:
                rendition = image.get_rendition(spec)

        assert rendition.filter_spec == spec
        get_many.assert_not_called()
        assert not any("rendition" in query["sql"].lower() for query in ctx.captured_queries)

    def test_attach_prefetched_renditions_on_fresh_image_instance(self):
        spec = "fill-150x100"
        self.image1.get_rendition(spec)
        fresh = type(self.image1).objects.get(pk=self.image1.pk)

        CMSPage._attach_prefetched_renditions([fresh])

        self._assert_get_rendition_skips_cache_and_sql(fresh, spec)

    def test_attach_prefetched_renditions_for_default_wagtail_image(self):
        spec = "fill-150x100"
        image = WagtailImage.objects.create(title="Default Image", file=get_test_image_file())
        image.get_rendition(spec)
        fresh = WagtailImage.objects.get(pk=image.pk)

        CMSPage._attach_prefetched_renditions([fresh])

        self._assert_get_rendition_skips_cache_and_sql(fresh, spec)

    def test_prefetch_stream_renditions_on_body_and_footer_instances(self):
        spec = "fill-150x100"
        self.image1.get_rendition(spec)
        self.image3.get_rendition(spec)
        page = CMSPage(title="Prefetch", body=[("hero", {"image": self.image1})])
        footer = CMSFooterPage(title="Footer", footer=[("info", {"image": self.image3})])

        page._prefetch_stream_renditions(page.body)
        page._prefetch_stream_renditions(footer.footer)

        self._assert_get_rendition_skips_cache_and_sql(page.body[0].value.get("image"), spec)
        self._assert_get_rendition_skips_cache_and_sql(footer.footer[0].value.get("image"), spec)
