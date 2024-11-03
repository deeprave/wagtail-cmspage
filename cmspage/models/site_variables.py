from django.core.cache import cache
from django.db import models
from wagtail.models import Site


class SiteVariables(models.Model):
    """
    SiteVariables Model

    This class represents the site variables model, which is used to store and manage
    custom variables for a specific site.

    Attributes:
        site (Site): The site associated with the variables.
        vars (dict): The dictionary of variables.
                     It is stored as a JSONField in the database.

    Meta:
        verbose_name (str): The human-readable name for the model.
    """

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="variables")
    vars = models.JSONField(blank=True, null=True, default=dict)

    @staticmethod
    def get_cached_variables(site: Site) -> dict:
        cache_key = f"site_variables:{site.id}"
        site_vars = cache.get(cache_key)
        if not site_vars:
            site_record = SiteVariables.objects.filter(site=site).first()
            site_vars = site_record.vars if site_record else {}
            cache.set(cache_key, site_vars, timeout=900)
        return site_vars

    @staticmethod
    def clear_cached_variables(site: Site):
        cache.delete(f"site_variables:{site.id}")

    class Meta:
        verbose_name = "Site Variables"
