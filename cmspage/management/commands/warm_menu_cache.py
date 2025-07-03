"""
Management command to warm the menu link cache for better performance.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Site

from cmspage.models import MenuLink


User = get_user_model()


class Command(BaseCommand):
    help = "Warm the menu link cache for all sites and common user scenarios"

    def add_arguments(self, parser):
        parser.add_argument(
            "--site-id",
            type=int,
            help="Warm cache for specific site ID only",
        )
        parser.add_argument(
            "--include-staff",
            action="store_true",
            help="Include staff users in cache warming",
        )

    def handle(self, *args, **options):
        sites = Site.objects.all()
        if options["site_id"]:
            sites = sites.filter(id=options["site_id"])

        if not sites.exists():
            self.stdout.write(
                self.style.ERROR("No sites found to warm cache for")
            )
            return

        for site in sites:
            self.stdout.write(f"Warming cache for site: {site.site_name} (ID: {site.id})")

            # Common user scenarios
            user_ids = [0]  # Anonymous user

            if options["include_staff"]:
                # Add staff users
                staff_users = User.objects.filter(
                    is_staff=True, is_active=True
                ).values_list("id", flat=True)[:10]  # Limit to prevent excessive cache usage
                user_ids.extend(staff_users)

            # Warm cache for all user scenarios
            MenuLink.warm_cache_for_site(site, user_ids)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Cache warmed for {len(user_ids)} user scenarios on site {site.site_name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully warmed menu cache for {sites.count()} site(s)"
            )
        )
