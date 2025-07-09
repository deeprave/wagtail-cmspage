"""
Performance monitoring utilities for cmspage.
"""

import time
import logging
from contextlib import contextmanager
from django.db import connection
from django.conf import settings

from cmspage.models import MenuLink

logger = logging.getLogger("cmspage.performance")


@contextmanager
def query_monitor(operation_name="database_operation"):
    """
    Context manager to monitor database queries and execution time.

    Usage:
        with query_monitor("menu_link_fetch"):
            menu_links = MenuLink.objects.all()
    """
    initial_queries = len(connection.queries)
    start_time = time.time()

    try:
        yield
    finally:
        end_time = time.time()
        final_queries = len(connection.queries)
        query_count = final_queries - initial_queries
        execution_time = end_time - start_time

        # Log performance metrics
        logger.info(f"Performance: {operation_name} - Queries: {query_count}, Time: {execution_time:.3f}s")

        # In debug mode, also log the actual queries
        if settings.DEBUG and query_count > 0:
            recent_queries = connection.queries[initial_queries:final_queries]
            for i, query in enumerate(recent_queries, 1):
                logger.debug(f"Query {i}: {query['sql'][:100]}...")


def analyze_menu_performance(site):
    """
    Analyze menu link performance for a specific site.

    Returns:
        dict: Performance metrics including query count and timing
    """
    from .models import MenuLink

    metrics = {}

    # Test the non-optimized approach
    with query_monitor("menu_links_basic"):
        basic_start = time.time()
        _ = list(MenuLink.objects.filter(site=site))
        basic_time = time.time() - basic_start
        metrics["basic"] = {
            "time": basic_time,
            "query_count": len(connection.queries) - len(metrics.get("_initial_queries", [])),
        }

    # Reset query count
    connection.queries_log.clear()

    # Test optimized approach
    with query_monitor("menu_links_optimized"):
        opt_start = time.time()
        _ = list(MenuLink.objects.get_optimized_queryset(site))
        opt_time = time.time() - opt_start
        metrics["optimized"] = {"time": opt_time, "query_count": len(connection.queries)}

    # Test the cached approach
    connection.queries_log.clear()
    with query_monitor("menu_links_cached"):
        cached_start = time.time()
        _ = MenuLink.get_cached_menu_links(site, 0)
        cached_time = time.time() - cached_start
        metrics["cached"] = {"time": cached_time, "query_count": len(connection.queries)}

    metrics["improvement"] = {
        "time_saved": basic_time - opt_time,
        "queries_saved": metrics["basic"]["query_count"] - metrics["optimized"]["query_count"],
    }

    return metrics


class MenuLinkQueryOptimizer:
    """
    Utility class to help optimize MenuLink queries.
    """

    @staticmethod
    def get_menu_links_with_metrics(site, user_id=0):
        """
        Get menu links with performance metrics.
        """
        with query_monitor(f"menu_links_site_{site.id}_user_{user_id}"):
            return MenuLink.get_cached_menu_links(site, user_id)

    @staticmethod
    def bulk_update_menu_order(site, link_order_map):
        """
        Efficiently update menu order for multiple links.

        Args:
            site: Site instance
            link_order_map: Dict mapping link_id to new menu_order
        """
        from django.db import transaction
        from .models import MenuLink

        with transaction.atomic():
            with query_monitor(f"bulk_update_menu_order_{len(link_order_map)}_links"):
                # Use bulk_update for efficiency
                links_to_update = []
                for link in MenuLink.objects.filter(site=site, id__in=link_order_map.keys()):
                    link.menu_order = link_order_map[link.id]
                    links_to_update.append(link)

                MenuLink.objects.bulk_update(links_to_update, ["menu_order"])

                # Clear cache after bulk update
                MenuLink.clear_cached_menu_links()

        return len(links_to_update)


def log_slow_queries(threshold_ms=100):
    """
    Decorator to log slow queries for a function.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            initial_queries = len(connection.queries)
            start_time = time.time()

            result = func(*args, **kwargs)

            end_time = time.time()
            execution_time_ms = (end_time - start_time) * 1000

            if execution_time_ms > threshold_ms:
                query_count = len(connection.queries) - initial_queries
                logger.warning(
                    f"Slow operation detected: {func.__name__} - "
                    f"Time: {execution_time_ms:.2f}ms, "
                    f"Queries: {query_count}"
                )

            return result

        return wrapper

    return decorator
