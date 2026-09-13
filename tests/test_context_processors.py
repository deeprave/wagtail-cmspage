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


def mock_menulink(id, title, url, parent_id=None, staff_only=False, link_type="Page"):
    menulink = Mock(spec=MenuLink)
    menulink.id = id
    menulink.parent_id = parent_id
    menulink.menu_title = title
    menulink.menu_link_title = title  # Add this property
    menulink.menu_link_icon = "page"
    menulink.menu_icon_color = "body"  # Add this property
    menulink.menu_link_type = link_type
    menulink.url = url
    menulink.staff_only = staff_only
    menulink.parent = Mock(spec=MenuLink, id=parent_id) if parent_id else None
    return menulink


def _nav_ids(items):
    ids = []
    for item in items:
        ids.append(item["id"])
        ids.extend(_nav_ids(item.get("children") or []))
    return ids


def _nav_titles(items):
    titles = []
    for item in items:
        titles.append(item["title"])
        titles.extend(_nav_titles(item.get("children") or []))
    return titles


@pytest.fixture
def inaccessible_user(request):
    if request.param == "anonymous":
        return AnonymousUser()
    return Mock(
        spec=User,
        is_authenticated=True,
        is_active=True,
        is_staff=False,
        is_superuser=False,
        pk=2,
        id=2,
    )


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


def test_cmspage_context_finds_site_once(mock_request, mock_site):
    """Test cmspage_context reuses the resolved Wagtail site"""
    with (
        patch("wagtail.models.Site.find_for_request", return_value=mock_site) as mock_find_site,
        patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[]),
    ):
        result = cmspage_context(mock_request)

    assert result["site"] == mock_site
    assert result["navigation"] == []
    mock_find_site.assert_called_once_with(mock_request)


def test_navigation_passes_request_to_menu_link_url(rf, mock_site):
    """Test navigation lets Wagtail cache page URL lookups on the request"""
    request = rf.get("/")
    request.user = AnonymousUser()
    link = mock_menulink(id=1, title="Home", url="/", parent_id=None)
    link.get_url.return_value = "/request-aware/"

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[link]):
        result = navigation(request)

    assert result["navigation"][0]["url"] == "/request-aware/"
    link.get_url.assert_called_once_with(site=mock_site, request=request)


def test_navigation_links_children_when_child_precedes_parent(rf):
    """Test navigation hierarchy assembly does not depend on link order"""
    request = rf.get("/")
    request.user = AnonymousUser()
    child = mock_menulink(id=2, title="Child", url="/parent/child/", parent_id=1)
    parent = mock_menulink(id=1, title="Parent", url="/parent/", parent_id=None)

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[child, parent]):
        result = navigation(request)

    assert result["navigation"] == [
        {
            "id": 1,
            "title": "Parent",
            "icon": "page",
            "icon_color": "body",
            "type": "Page",
            "url": "/parent/",
            "children": [
                {
                    "id": 2,
                    "title": "Child",
                    "icon": "page",
                    "icon_color": "body",
                    "type": "Page",
                    "url": "/parent/child/",
                    "children": [],
                }
            ],
        }
    ]


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


@pytest.mark.parametrize("inaccessible_user", ["anonymous", "authenticated_non_staff"], indirect=True)
def test_navigation_excludes_children_of_staff_only_parent(rf, inaccessible_user):
    """A hidden staff-only parent removes its descendants from the visible menu."""
    parent = mock_menulink(id=10, title="Admin", url="/admin/", parent_id=None, staff_only=True)
    child = mock_menulink(
        id=23,
        title="ContactUs",
        url="https://rjf.org.au/admin/django/rjf/contactus/",
        parent_id=10,
        link_type="URL",
    )
    public = mock_menulink(id=1, title="Home", url="/", parent_id=None)
    request = rf.get("/")
    request.user = inaccessible_user

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[parent, child, public]):
        result = navigation(request)

    assert _nav_ids(result["navigation"]) == [1]
    assert _nav_titles(result["navigation"]) == ["Home"]


@pytest.mark.parametrize("inaccessible_user", ["anonymous", "authenticated_non_staff"], indirect=True)
def test_navigation_excludes_staff_only_child_of_visible_parent(rf, inaccessible_user):
    """A visible parent stays; its staff-only child and descendants do not."""
    public_parent = mock_menulink(id=2, title="About", url="/about/", parent_id=None)
    staff_child = mock_menulink(id=10, title="Admin", url="/admin/", parent_id=2, staff_only=True)
    grandchild = mock_menulink(
        id=23,
        title="ContactUs",
        url="https://rjf.org.au/admin/django/rjf/contactus/",
        parent_id=10,
        link_type="URL",
    )
    public = mock_menulink(id=1, title="Home", url="/", parent_id=None)
    request = rf.get("/")
    request.user = inaccessible_user

    with patch(
        "cmspage.context_processors.MenuLink.get_cached_menu_links",
        return_value=[public, public_parent, staff_child, grandchild],
    ):
        result = navigation(request)

    assert _nav_ids(result["navigation"]) == [1, 2]
    assert _nav_titles(result["navigation"]) == ["Home", "About"]
    assert result["navigation"][1]["children"] == []


def test_navigation_excludes_descendants_when_inaccessible_parent_is_listed_last(rf):
    """Descendants stay hidden even when they appear before their inaccessible parent."""
    child = mock_menulink(
        id=23,
        title="ContactUs",
        url="https://rjf.org.au/admin/django/rjf/contactus/",
        parent_id=10,
        link_type="URL",
    )
    grandchild = mock_menulink(id=24, title="Messages", url="/admin/messages/", parent_id=23, link_type="URL")
    parent = mock_menulink(id=10, title="Admin", url="/admin/", parent_id=None, staff_only=True)
    public = mock_menulink(id=1, title="Home", url="/", parent_id=None)
    request = rf.get("/")
    request.user = AnonymousUser()

    with patch(
        "cmspage.context_processors.MenuLink.get_cached_menu_links",
        return_value=[child, grandchild, parent, public],
    ):
        result = navigation(request)

    assert _nav_ids(result["navigation"]) == [1]
    assert _nav_titles(result["navigation"]) == ["Home"]


def test_navigation_includes_staff_only_branch_for_staff(rf):
    parent = mock_menulink(id=10, title="Admin", url="/admin/", parent_id=None, staff_only=True)
    child = mock_menulink(
        id=23,
        title="ContactUs",
        url="https://rjf.org.au/admin/django/rjf/contactus/",
        parent_id=10,
        link_type="URL",
    )
    request = rf.get("/")
    request.user = Mock(
        spec=User,
        is_authenticated=True,
        is_active=True,
        is_staff=True,
        is_superuser=False,
        pk=1,
        id=1,
    )

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[parent, child]):
        result = navigation(request)

    assert _nav_ids(result["navigation"]) == [10, 23]
    assert _nav_titles(result["navigation"]) == ["Admin", "ContactUs"]
    assert result["navigation"][0]["children"][0]["title"] == "ContactUs"


def test_navigation_excludes_items_whose_parent_is_missing(rf):
    child = mock_menulink(id=23, title="ContactUs", url="/missing-parent/", parent_id=99, link_type="URL")
    public = mock_menulink(id=1, title="Home", url="/", parent_id=None)
    request = rf.get("/")
    request.user = AnonymousUser()

    with patch("cmspage.context_processors.MenuLink.get_cached_menu_links", return_value=[child, public]):
        result = navigation(request)

    assert _nav_ids(result["navigation"]) == [1]
    assert _nav_titles(result["navigation"]) == ["Home"]


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

    def test_navigation_excludes_children_of_staff_only_parent(self, rf):
        """A hidden staff-only parent removes its descendants from the visible menu."""
        from django.core.cache import cache
        from wagtail.models import Site

        site = Site.objects.first() or Site.objects.create(hostname="localhost", port=80, site_name="Test Site")
        parent = MenuLink.objects.create(
            site=site,
            menu_title="Admin",
            link_url="/admin/",
            menu_order=1,
            staff_only=True,
        )
        MenuLink.objects.create(
            site=site,
            menu_title="ContactUs",
            link_url="https://rjf.org.au/admin/django/rjf/contactus/",
            parent=parent,
            menu_order=1,
        )
        MenuLink.objects.create(site=site, menu_title="Home", link_url="/", menu_order=2)

        request = rf.get("/")
        request.user = AnonymousUser()
        cache.clear()

        with patch("wagtail.models.Site.find_for_request", return_value=site):
            result = navigation(request)

        created = {"Home", "Admin", "ContactUs"}
        assert [title for title in _nav_titles(result["navigation"]) if title in created] == ["Home"]
