import pytest
from unittest.mock import patch
from django.test import TestCase
from django.db import connection
from django.test.utils import override_settings
from wagtail.models import Site

from cmspage.models import MenuLink
from cmspage.performance import query_monitor, analyze_menu_performance


@pytest.mark.django_db
class TestMenuLinkPerformance:
    """Test performance optimizations for MenuLink"""

    @pytest.fixture
    def site(self):
        from wagtail.models import Page
        try:
            # Try to get existing default site
            return Site.objects.get(is_default_site=True)
        except Site.DoesNotExist:
            # Create a root page first
            root_page = Page.objects.create(
                title="Root",
                slug="root",
                path="0001",
                depth=1,
                numchild=0,
                url_path="/"
            )
            return Site.objects.create(
                hostname="testsite.com",
                site_name="Test Site",
                root_page=root_page,
                is_default_site=True
            )

    @pytest.fixture
    def menu_structure(self, site):
        """Create a hierarchical menu structure for testing"""
        # Create parent links
        parent1 = MenuLink.objects.create(
            site=site,
            menu_title="Products",
            link_url="/products/",
            menu_order=1
        )
        parent2 = MenuLink.objects.create(
            site=site,
            menu_title="Services",
            link_url="/services/",
            menu_order=2
        )

        # Create child links
        children = []
        for i in range(5):
            child = MenuLink.objects.create(
                site=site,
                menu_title=f"Product {i+1}",
                link_url=f"/products/product-{i+1}/",
                parent=parent1,
                menu_order=i+1
            )
            children.append(child)

        for i in range(3):
            child = MenuLink.objects.create(
                site=site,
                menu_title=f"Service {i+1}",
                link_url=f"/services/service-{i+1}/",
                parent=parent2,
                menu_order=i+1
            )
            children.append(child)

        return {"parents": [parent1, parent2], "children": children}

    def test_optimized_queryset_reduces_queries(self, site, menu_structure):
        """Test that optimized queryset reduces database queries"""
        # Clear any existing queries
        connection.queries_log.clear()

        # Count queries with optimized approach
        initial_query_count = len(connection.queries)
        optimized_links = list(MenuLink.objects.get_optimized_queryset(site))
        optimized_query_count = len(connection.queries) - initial_query_count

        # Should use select_related to minimize queries
        assert optimized_query_count <= 2, f"Expected <= 2 queries, got {optimized_query_count}"
        assert len(optimized_links) == 10  # 2 parents + 8 children

        # Test that related objects are prefetched (no additional queries)
        initial_query_count = len(connection.queries)
        for link in optimized_links:
            _ = link.site.hostname  # Should not trigger additional query
            if link.parent:
                _ = link.parent.menu_title  # Should not trigger additional query
        final_query_count = len(connection.queries) - initial_query_count

        assert final_query_count == 0, f"Related object access triggered {final_query_count} additional queries"

    @patch("cmspage.models.menu_link.MenuLink.cache_enabled", True)
    def test_cached_menu_links_performance(self, site, menu_structure):
        """Test that cached menu links work correctly when caching is enabled"""
        # Test that the cached method returns results
        result = MenuLink.get_cached_menu_links(site, 0)

        # Should return menu links from the menu_structure fixture
        assert len(result) == 10  # 2 parents + 8 children
        assert all(isinstance(link, MenuLink) for link in result)

        # Test with different user_id
        result2 = MenuLink.get_cached_menu_links(site, 1)
        assert len(result2) == 10

    def test_bulk_create_efficiency(self, site):
        """Test that bulk create is more efficient than individual creates"""
        menu_data = [
            {"menu_title": f"Bulk Item {i}", "link_url": f"/bulk/{i}/", "menu_order": i}
            for i in range(10)
        ]

        connection.queries_log.clear()
        initial_query_count = len(connection.queries)

        created_links = MenuLink.bulk_create_menu_links(menu_data, site)

        bulk_query_count = len(connection.queries) - initial_query_count

        # Bulk create should use significantly fewer queries than individual creates
        # Expected: 1 bulk insert + possible cache clear operations
        assert bulk_query_count <= 5, f"Bulk create used {bulk_query_count} queries (expected <= 5)"
        assert len(created_links) == 10

    @override_settings(DEBUG=True)
    def test_query_monitor_functionality(self, site, menu_structure, caplog):
        """Test that query monitoring works correctly"""
        import logging

        # Set logging level for cmspage.performance logger
        caplog.set_level(logging.INFO, logger="cmspage.performance")

        with query_monitor("test_operation"):
            MenuLink.objects.get_optimized_queryset(site).count()

        # Should have logged performance metrics
        assert len(caplog.records) > 0
        log_message = caplog.records[0].message
        assert "test_operation" in log_message
        assert "Queries:" in log_message
        assert "Time:" in log_message

    def test_hierarchy_building_efficiency(self, site, menu_structure):
        """Test that hierarchy building is efficient"""
        connection.queries_log.clear()
        initial_query_count = len(connection.queries)

        # Get hierarchical structure
        hierarchy_links = MenuLink.objects.get_hierarchy_optimized(site)
        hierarchy_query_count = len(connection.queries) - initial_query_count

        # Should use minimal queries for hierarchy building
        assert hierarchy_query_count <= 3, f"Hierarchy building used {hierarchy_query_count} queries"

        # Verify hierarchy is correctly built
        links_list = list(hierarchy_links)
        assert len(links_list) == 10

        # Parents should come before their children in the ordered list
        parent_indices = {}
        for i, link in enumerate(links_list):
            if not link.parent:
                parent_indices[link.id] = i

        for i, link in enumerate(links_list):
            if link.parent and link.parent.id in parent_indices:
                parent_index = parent_indices[link.parent.id]
                assert i > parent_index, "Child should come after parent in hierarchy"


class TestPerformanceAnalysis(TestCase):
    """Test performance analysis utilities"""

    def setUp(self):
        try:
            # Try to get existing default site
            self.site = Site.objects.get(is_default_site=True)
        except Site.DoesNotExist:
            from wagtail.models import Page
            # Create a root page first
            root_page = Page.objects.create(
                title="Root",
                slug="root",
                path="0001",
                depth=1,
                numchild=0,
                url_path="/"
            )
            self.site = Site.objects.create(
                hostname="testsite.com",
                site_name="Test Site",
                root_page=root_page,
                is_default_site=True
            )

        # Create some menu links
        for i in range(5):
            MenuLink.objects.create(
                site=self.site,
                menu_title=f"Link {i}",
                link_url=f"/link-{i}/",
                menu_order=i
            )

    @override_settings(DEBUG=True)
    def test_analyze_menu_performance(self):
        """Test the performance analysis function"""
        metrics = analyze_menu_performance(self.site)

        # Should return metrics for different approaches
        assert "basic" in metrics
        assert "optimized" in metrics
        assert "cached" in metrics
        assert "improvement" in metrics

        # Optimized should perform better than basic
        assert metrics["optimized"]["query_count"] <= metrics["basic"]["query_count"]

        # Cached should be fastest (may be 0 queries on second call)
        assert metrics["cached"]["query_count"] <= metrics["optimized"]["query_count"]
