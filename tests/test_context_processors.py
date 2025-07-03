import pytest
from unittest.mock import Mock, patch

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from wagtail.models import Site
from cmspage.context_processors import navigation, cmspage_context
from cmspage.models import MenuLink

User = get_user_model()


@pytest.fixture
def mock_site():
    return Mock(spec=Site, id=1, _state=Mock(db="default"))


@pytest.fixture
def mock_request(mock_site):
    request = Mock(spec=HttpRequest)
    request.user = Mock(spec=User)
    request.user.is_authenticated = True
    request.user.id = 1
    request.site = mock_site
    return request


@pytest.fixture(autouse=True)
def mock_site_find_for_request(mock_site):
    with patch("wagtail.models.Site.find_for_request", return_value=mock_site):
        yield


def mock_menulink(id, title, url, parent_id=None):
    menulink = Mock(spec=MenuLink)
    menulink.id = id
    menulink.menu_title = title
    menulink.menu_link_title = title  # Add this property
    menulink.menu_link_icon = "page"
    menulink.menu_icon_color = "body"  # Add this property
    menulink.menu_link_type = "Page"
    menulink.url = url
    menulink.staff_only = False  # Add this property
    menulink.parent = Mock(spec=MenuLink, id=parent_id) if parent_id else None
    return menulink


@pytest.mark.parametrize(
    "user_authenticated, user_id, menulink_records, expected_navigation",
    [
        (
            False,
            None,
            [
                mock_menulink(id=1, title="Home", url="/", parent_id=None),
                mock_menulink(id=2, title="About", url="/about/", parent_id=None),
                mock_menulink(id=4, title="Team", url="/about/team/", parent_id=2),
                mock_menulink(id=5, title="History", url="/about/history/", parent_id=2),
                mock_menulink(id=3, title="Contact", url="/contact/", parent_id=None),
            ],
            [
                {
                    "id": 1,
                    "title": "Home",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/",
                    "children": [],
                },
                {
                    "id": 2,
                    "title": "About",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/about/",
                    "children": [
                        {
                            "id": 4,
                            "title": "Team",
                            "icon": "page",
                            "icon_color": "body",
                            "type": "Page",
                            "url": "/about/team/",
                            "children": [],
                        },
                        {
                            "id": 5,
                            "title": "History",
                            "icon": "page",
                            "icon_color": "body",
                            "type": "Page",
                            "url": "/about/history/",
                            "children": [],
                        },
                    ],
                },
                {
                    "id": 3,
                    "title": "Contact",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/contact/",
                    "children": [],
                },
            ],
        ),
        (
            True,
            1,
            [
                mock_menulink(id=1, title="Home", url="/", parent_id=None),
                mock_menulink(id=2, title="Dashboard", url="/dashboard/", parent_id=None),
                mock_menulink(id=3, title="Logout", url="/logout/", parent_id=None),
            ],
            [
                {
                    "id": 1,
                    "title": "Home",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/",
                    "children": [],
                },
                {
                    "id": 2,
                    "title": "Dashboard",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/dashboard/",
                    "children": [],
                },
                {
                    "id": 3,
                    "title": "Logout",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/logout/",
                    "children": [],
                },
            ],
        ),
    ],
    ids=["anonymous_user", "authenticated_user"],
)
def test_navigation(user_authenticated, user_id, menulink_records, expected_navigation, rf):
    request = rf.get("/")
    request.user = User(id=user_id) if user_authenticated else AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=menulink_records):
        result = navigation(request)
        assert result["navigation"] == expected_navigation


def test_cmspage_context(mock_request):
    """Test cmspage_context returns navigation data"""
    # Create mock menu links
    links = [
        mock_menulink(id=1, title="Home", url="/", parent_id=None),
        mock_menulink(id=2, title="About", url="/about/", parent_id=None),
    ]

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=links):
        result = cmspage_context(mock_request)

        assert "navigation" in result
        assert len(result["navigation"]) == 2
        assert result["navigation"][0]["title"] == "Home"


def test_navigation_with_circular_reference(rf):
    """Test navigation handling with circular parent references"""
    # Create menu links with potential circular reference
    link1 = mock_menulink(id=1, title="Link 1", url="/1/", parent_id=2)
    link2 = mock_menulink(id=2, title="Link 2", url="/2/", parent_id=1)

    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[link1, link2]):
        # Should handle circular references without infinite loop
        result = navigation(request)
        assert "navigation" in result
        assert isinstance(result["navigation"], list)


def test_navigation_with_none_parent(rf):
    """Test navigation with None parent reference"""
    # Create a menu link where parent.id might be accessed on None
    link = mock_menulink(id=1, title="Test", url="/test/", parent_id=None)
    link.parent = None  # Explicitly set to None

    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[link]):
        result = navigation(request)
        assert result["navigation"] == [
            {
                "id": 1,
                "title": "Test",
                "icon": "page",
                "icon_color": "body",
                "type": "Page",
                "url": "/test/",
                "children": [],
            }
        ]


def test_navigation_with_deep_nesting(rf):
    """Test navigation with deeply nested menu structure"""
    # Create deeply nested menu links
    links = []
    for i in range(10):
        parent_id = i if i > 0 else None
        link = mock_menulink(id=i + 1, title=f"Level {i}", url=f"/level{i}/", parent_id=parent_id)
        links.append(link)

    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=links):
        result = navigation(request)

        # Check that the structure is properly nested
        nav = result["navigation"]
        assert len(nav) == 1  # Only root item

        # Traverse the nested structure
        current = nav[0]
        for i in range(9):
            assert current["title"] == f"Level {i}"
            if i < 8:
                assert len(current["children"]) == 1
                current = current["children"][0]


def test_navigation_empty_menu_links(rf):
    """Test navigation with no menu links"""
    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[]):
        result = navigation(request)
        assert result["navigation"] == []


def test_navigation_with_missing_site(rf):
    """Test navigation when site is not found"""
    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("wagtail.models.Site.find_for_request", return_value=None):
        with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[]):
            result = navigation(request)
            assert result["navigation"] == []


def test_navigation_menu_link_attributes(rf):
    """Test that all menu link attributes are properly transferred"""
    link = Mock(spec=MenuLink)
    link.id = 123
    link.menu_title = "Custom Title"
    link.menu_link_icon = "custom-icon"
    link.menu_icon_color = "primary"  # Add this property
    link.menu_link_type = "External"
    link.menu_link_title = "Custom Title"  # Add this property
    link.url = "https://example.com"
    link.staff_only = False  # Add this property
    link.parent = None

    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[link]):
        result = navigation(request)
        nav_item = result["navigation"][0]

        assert nav_item["id"] == 123
        assert nav_item["title"] == "Custom Title"
        assert nav_item["icon"] == "custom-icon"
        assert nav_item["icon_color"] == "primary"
        assert nav_item["type"] == "External"
        assert nav_item["url"] == "https://example.com"
        assert nav_item["children"] == []


@pytest.mark.django_db
def test_site_variables_function(rf):
    """Test site_variables context processor"""
    from cmspage.context_processors import site_variables
    from wagtail.models import Site, Page

    # Use existing root page or create one with unique path
    try:
        root_page = Page.objects.get(pk=1)
    except Page.DoesNotExist:
        root_page = Page.objects.create(title="Test Root", slug="test-root", path="0002", depth=1, numchild=0)

    site = Site.objects.create(
        hostname="testsite.com",
        site_name="Test Site",
        root_page=root_page,
        is_default_site=False,  # Don't conflict with existing default
    )

    request = rf.get("/")
    with patch("wagtail.models.Site.find_for_request", return_value=site):
        result = site_variables(request)

    assert "site" in result
    assert "site_name" in result
    assert "site_hostname" in result
    assert "site_is_default" in result

    assert result["site"] == site
    assert result["site_name"] == "Test Site"
    assert result["site_hostname"] == "testsite.com"
    assert result["site_is_default"] is False


def test_site_variables_no_site(rf):
    """Test site_variables when no site is found"""
    from cmspage.context_processors import site_variables
    from wagtail.models import Site

    request = rf.get("/")
    with patch("wagtail.models.Site.find_for_request", side_effect=Site.DoesNotExist):
        result = site_variables(request)

    assert "site" in result
    assert "site_name" in result
    assert "site_hostname" in result
    assert "site_is_default" in result

    assert result["site"] is None
    assert result["site_name"] == ""
    assert result["site_hostname"] == ""
    assert result["site_is_default"] is False


@pytest.mark.django_db
class TestNavigationIntegration:
    """Integration tests for navigation with real database"""

    def test_navigation_with_real_menulinks(self, rf, db):
        """Test navigation with actual MenuLink objects"""
        # Create real MenuLink objects
        from wagtail.models import Site

        site = Site.objects.first() or Site.objects.create(hostname="localhost", port=80, site_name="Test Site")

        # Patch the Site.find_for_request to return our real site instead of the mock
        with patch("wagtail.models.Site.find_for_request", return_value=site):
            parent = MenuLink.objects.create(site=site, menu_title="Parent", link_url="/parent/", menu_order=1)
            _ = MenuLink.objects.create(site=site, menu_title="Child", link_url="/child/", parent=parent, menu_order=1)

            request = rf.get("/")
            request.user = AnonymousUser()

            # Clear cache to ensure fresh data
            from django.core.cache import cache

            cache.clear()

            result = navigation(request)

            # Verify structure
            assert len(result["navigation"]) >= 1

            # Find our parent link
            parent_nav = None
            for item in result["navigation"]:
                if item["title"] == "Parent":
                    parent_nav = item
                    break

            assert parent_nav is not None
            assert len(parent_nav["children"]) == 1
            assert parent_nav["children"][0]["title"] == "Child"
