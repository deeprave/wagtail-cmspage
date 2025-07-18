import pytest
from unittest.mock import MagicMock

from wagtail.images.tests.utils import get_test_image_file

from cmspage.models import CMSPage, CMSPageImage


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

    def test_image_id_deduplication(self):
        # sourcery skip: extract-duplicate-method
        """Test that image IDs are deduplicated when prefetching"""
        # Create duplicate image IDs
        duplicate_ids = [self.image1.id, self.image1.id, self.image2.id]
        deduped_ids = list(set(duplicate_ids))

        # Verify deduplication
        assert len(duplicate_ids) == 3
        assert len(deduped_ids) == 2
        assert self.image1.id in deduped_ids
        assert self.image2.id in deduped_ids

        # Test that CMSPageImage.objects.filter works with the deduplicated IDs
        images = CMSPageImage.objects.filter(id__in=deduped_ids)
        assert images.count() == 2

        # Create a dictionary mapping image IDs to images
        image_dict = {img.id: img for img in images}
        assert len(image_dict) == 2
        assert self.image1.id in image_dict
        assert self.image2.id in image_dict

    def test_extract_and_prefetch_integration(self):
        """Test the integration of image extraction and prefetching"""
        # Test extraction from different block types
        cards_ids = CMSPage._extract_image_ids_from_block(
            MagicMock(block_type="cards", value={"cards": [{"image": self.image1}, {"image": self.image2}]})
        )

        carousel_ids = CMSPage._extract_image_ids_from_block(
            MagicMock(
                block_type="carousel",
                value={"carousel": [{"carousel_image": self.image2}, {"carousel_image": self.image3}]},
            )
        )

        image_text_ids = CMSPage._extract_image_ids_from_block(
            MagicMock(block_type="image_and_text", value={"image": self.image1})
        )

        # Combine all IDs
        all_ids = cards_ids + carousel_ids + image_text_ids

        # Verify extraction worked correctly
        assert len(cards_ids) == 2
        assert len(carousel_ids) == 2
        assert len(image_text_ids) == 1
        assert len(all_ids) == 5  # Total with duplicates

        # Deduplicate IDs
        deduped_ids = list(set(all_ids))
        assert len(deduped_ids) == 3  # Should be 3 unique IDs

        # Fetch images using the deduplicated IDs
        images = CMSPageImage.objects.filter(id__in=deduped_ids)
        assert images.count() == 3

        # Create a dictionary mapping image IDs to images (simulating _prefetched_images)
        prefetched_images = {img.id: img for img in images}
        assert len(prefetched_images) == 3
        assert self.image1.id in prefetched_images
        assert self.image2.id in prefetched_images
        assert self.image3.id in prefetched_images
