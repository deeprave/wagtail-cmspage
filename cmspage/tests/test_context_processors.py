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
    menulink.menu_link_icon = "page"
    menulink.menu_link_type = "Page"
    menulink.url = url
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
                {"id": 1, "title": "Home", "icon": "page", "type": "Page", "url": "/", "children": []},
                {
                    "id": 2,
                    "title": "About",
                    "icon": "page",
                    "type": "Page",
                    "url": "/about/",
                    "children": [
                        {
                            "id": 4,
                            "title": "Team",
                            "icon": "page",
                            "type": "Page",
                            "url": "/about/team/",
                            "children": [],
                        },
                        {
                            "id": 5,
                            "title": "History",
                            "icon": "page",
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
                {"id": 1, "title": "Home", "icon": "page", "type": "Page", "url": "/", "children": []},
                {"id": 2, "title": "Dashboard", "icon": "page", "type": "Page", "url": "/dashboard/", "children": []},
                {"id": 3, "title": "Logout", "icon": "page", "type": "Page", "url": "/logout/", "children": []},
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


@patch("cmspage.context_processors.navigation")
@patch("cmspage.context_processors.site_variables")
def test_cmspage_context(mock_site_variables, mock_navigation, mock_request):
    # Arrange
    mock_navigation.return_value = {"navigation": "nav_data"}
    mock_site_variables.return_value = {"site": "site_data"}

    # Act
    result = cmspage_context(mock_request)

    # Assert
    assert result == {"navigation": "nav_data", "site": "site_data"}
