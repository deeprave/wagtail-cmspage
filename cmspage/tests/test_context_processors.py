import pytest
from unittest.mock import Mock, patch
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


@pytest.mark.parametrize(
    "user_authenticated, user_id, expected_navigation",
    [
        (True, 1, [{"title": "Home", "type": "URL", "url": "/home"}]),
        (False, 0, []),
    ],
    ids=["authenticated_user", "unauthenticated_user"],
)
@patch("cmspage.context_processors.MenuLink.get_cached_menu_links")
def test_navigation(
    mock_get_cached_menu_links,
    user_authenticated,
    user_id,
    expected_navigation,
    mock_request,
    mock_site,
):
    # Arrange
    mock_request.user.is_authenticated = user_authenticated
    mock_request.user.id = user_id
    mock_get_cached_menu_links.return_value = (
        [MenuLink(id=1, site=mock_site, menu_title="Home", link_url="/home")] if user_authenticated else []
    )

    # Act
    result = navigation(mock_request)

    # Assert
    assert result["navigation"] == expected_navigation


@patch("cmspage.context_processors.navigation")
@patch("cmspage.context_processors.site_variables")
def test_cmspage_context(mock_site_variables, mock_events, mock_navigation, mock_request):
    # Arrange
    mock_navigation.return_value = {"navigation": "nav_data"}
    mock_events.return_value = {"events": "event_data"}
    mock_site_variables.return_value = {"site": "site_data"}

    # Act
    result = cmspage_context(mock_request)

    # Assert
    assert result == {"navigation": "nav_data", "site": "site_data"}
