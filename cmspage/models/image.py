import os

from PIL import Image as WillowImage
from wagtail.images.models import Image as WagtailImage


# This is optional but to activate this feature, you need to add the following to your settings.py
# in order to take advantage of converting images to WebP format when imported instead of when rendering the page.
# WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'
# Using this model will autoconvert images to WebP format as they are uploaded to the CMS.

class CMSPageImage(WagtailImage):
    def save(self, *args, **kwargs):
        # Check if this is a WebP file already
        if self.file and self.file.name and not self.file.name.lower().endswith(".webp"):
            # Call the original save method to save the image first
            super().save(*args, **kwargs)

            try:
                # Get the original image path
                original_image_path = self.file.path

                # Open the original image using PIL and convert to WebP
                with WillowImage.open(original_image_path) as image:
                    # Define the new path for the WebP image
                    webp_image_path = f"{os.path.splitext(original_image_path)[0]}.webp"
                    # Save the image in WebP format
                    image.save(webp_image_path, "WEBP")

                    # Update the file field to the new WebP path
                    from django.core.files.base import ContentFile
                    with open(webp_image_path, "rb") as webp_file:
                        webp_content = ContentFile(webp_file.read())
                        webp_filename = f"{os.path.splitext(self.file.name)[0]}.webp"
                        self.file.save(webp_filename, webp_content, save=False)

                    # Clean up the original WebP file
                    os.remove(webp_image_path)

            except Exception as e:
                # If WebP conversion fails, just use the original file but log the exception
                import logging
                logger = logging.getLogger(__name__)
                logger.warning("WebP conversion failed for %s: %s", self.file.name, e, exc_info=True)
        else:
            # For WebP files or files without a name, just save normally
            super().save(*args, **kwargs)

    class Meta:
        app_label = "cmspage"
