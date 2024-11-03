import os

from PIL import Image as WillowImage
from wagtail.images.models import Image as WagtailImage


# This is optional but to activate this feature, you need to add the following to your settings.py
# in order to take advantage of converting images to WebP format when imported instead of when rendering the page.
# WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'
# Using this model will autoconvert images to WebP format as they are uploaded to the CMS.

class CMSPageImage(WagtailImage):
    def save(self, *args, **kwargs):
        # Call the original save method to save the image first
        super().save(*args, **kwargs)

        # Get the original image path
        original_image_path = self.file.path

        # Open the original image using PIL
        with WillowImage.open(original_image_path) as image:
            # Define the new path for the WebP image
            webp_image_path = f"{os.path.splitext(original_image_path)[0]}.webp"
            # Save the image in WebP format
            image.save(webp_image_path, "WEBP")

        # Optionally, update the file field to the new WebP path, if required
        self.file.name = f"{os.path.splitext(self.file.name)[0]}.webp"
        super().save(*args, **kwargs)  # Save again to update the file name
