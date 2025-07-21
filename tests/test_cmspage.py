import pytest

from django.utils.text import slugify
from django.http import HttpRequest
from cmspage.models import CMSPage

from cmspage.models.functional import set_functional_cache


@pytest.fixture(scope="session", autouse=True)
def disable_functional_cache():
    set_functional_cache(False)
    yield
    set_functional_cache(True)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title,expected",
    [
        pytest.param("", "", id="empty-title"),
        pytest.param("a" * 256, "a" * 256, id="very-long-title"),
        pytest.param(
            "Title with special characters !@#$%^&*()", "Title with special characters !@#$%^&*()", id="special-chars"
        ),
        pytest.param("Test Page", "Test Page", id="first-title"),
        pytest.param("Another Page", "Another Page", id="second-title"),
    ],
)
def test_can_create_cmspage_with_title(title, expected):
    page = CMSPage(title=title)
    assert page.title == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "template_styles,expected_template",
    [
        pytest.param(None, "cmspage/cms_page.html", id="no-styles"),
        pytest.param("bootstrap5", "cmspage/bootstrap5/cms_page.html", id="bootstrap5-style"),
        pytest.param("tailwind", "cmspage/cms_page.html", id="tailwind-style"),
        pytest.param("mywebsite,bootstrap5", "cmspage/mywebsite/bootstrap5/cms_page.html", id="mywebsite-bootstrap5"),
        pytest.param("mywebsite tailwind", "cmspage/mywebsite/tailwind/cms_page.html", id="mywebsite-tailwind"),
        pytest.param("mywebsite2,bootstrap5", "cmspage/bootstrap5/cms_page.html", id="mywebsite2-bootstrap5"),
        pytest.param("mywebsite2 tailwind", "cmspage/cms_page.html", id="mywebsite2-tailwind"),
        pytest.param("mywebsite2 framework", "cmspage/cms_page.html", id="mywebsite2-framework"),
    ],
)
def test_get_template(rf, settings, template_styles, expected_template):
    # Arrange
    settings.CMSPAGE_TEMPLATE_STYLES = template_styles
    page = CMSPage(title="Test Page")
    page.pk = 1
    request = rf.get("/")

    # Act
    template = page.get_template(request)

    # Assert
    assert template == expected_template


@pytest.mark.django_db
@pytest.mark.parametrize(
    "include_names, expected_includes",
    [
        pytest.param(
            None,
            [
                "title",
                "header",
                "logo",
                "navigation",
                "navigation_item",
                "navigation_top",
                "navigation_top_item",
                "navigation_side",
                "navigation_side_item",
                "messages",
                "carousel",
                "main",
                "footer",
                "links",
                "contact",
                "media",
                "theme_switcher",
            ],
            id="default-includes",
        ),
        pytest.param("custom1,custom2", ["custom1", "custom2"], id="comma-separated-includes"),
        pytest.param("custom1 custom2", ["custom1", "custom2"], id="space-separated-includes"),
    ],
)
def test_include_templates(settings, include_names, expected_includes):
    # Arrange
    settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = include_names
    page = CMSPage(title="Test Page")
    page.pk = 1

    # Act
    includes = page.get_include_templates()

    # Assert
    assert list(includes.keys()) == expected_includes


@pytest.mark.django_db
@pytest.mark.parametrize(
    "base_name, base_path, expected_path",
    [
        pytest.param(
            None,
            None,
            "cmspage/cmspage.html",
            id="default-base",
        ),
        pytest.param(
            "cmspage.html",
            None,
            "cmspage/cmspage.html",
            id="explicit-base",
        ),
        pytest.param(
            "index.html",
            None,
            "cmspage/index.html",
            id="overridden-base",
        ),
        pytest.param(
            "/layout.html",
            None,
            "layout.html",
            id="no-path-base",
        ),
        pytest.param(
            "/layout/cmspage.html",
            None,
            "layout/cmspage.html",
            id="absolute-base",
        ),
        pytest.param(
            None,
            "pages",
            "pages/cmspage.html",
            id="pages-default-base",
        ),
        pytest.param("cmspage.html", "pages", "pages/cmspage.html", id="pages-explicit-base"),
        pytest.param(
            "index.html",
            "pages",
            "pages/index.html",
            id="pages-overridden-base",
        ),
        pytest.param(
            "/layout.html",
            "pages",
            "layout.html",
            id="pages-no-path-base",
        ),
        pytest.param(
            "/layout/cmspage.html",
            "pages",
            "layout/cmspage.html",
            id="pages-absolute-base",
        ),
    ],
)
def test_base_template(settings, base_name, base_path, expected_path):
    # Arrange
    settings.CMSPAGE_TEMPLATE_BASE = base_name
    settings.CMSPAGE_TEMPLATE_BASE_DIR = base_path
    page = CMSPage(title="Test Page", slug=slugify("Test Page"))
    page.pk = 1

    # Act
    base_template = page.base_template

    # Assert
    assert base_template == expected_path


@pytest.mark.django_db
def test_cmspage_get_context_default(settings):
    """Test CMSPage get_context with default settings"""
    # Disable caching to avoid interference between tests
    from cmspage.models import functional
    original_cache_state = functional.cache_state
    functional.cache_state = False

    title = "Test Page"
    base_name = None
    expected_base = "cmspage/cmspage.html"
    include_names = "header,main,footer"
    expected_includes = {
        "header": "cmspage/includes/header.html",
        "main": "cmspage/includes/main.html",
        "footer": "cmspage/includes/footer.html",
    }

    settings.CMSPAGE_TEMPLATE_BASE = base_name
    settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = include_names

    # Create a CMSPage instance
    page = CMSPage(title=title, slug=slugify(title))
    page.pk = 1

    # Create a HttpRequest instance
    request = HttpRequest()

    # Call the get_context method
    context = page.get_context(request)

    # Check that the context contains the expected keys
    assert "base_template" in context
    assert "include" in context
    assert "page" in context
    assert "request" in context

    # Check that the context contains the correct values
    assert context["page"] == page
    assert context["request"] == request
    assert context["base_template"] == expected_base
    assert context["include"] == expected_includes

    # Restore original cache state
    functional.cache_state = original_cache_state


@pytest.mark.django_db
def test_cmspage_get_context_explicit(settings):
    """Test CMSPage get_context with explicit settings"""
    # Disable caching to avoid interference between tests
    from cmspage.models import functional
    original_cache_state = functional.cache_state
    functional.cache_state = False

    title = "Another Page"
    base_name = "/cmspage.html"
    expected_base = "cmspage.html"
    include_names = "header,navigation,footer"
    expected_includes = {
        "header": "cmspage/includes/header.html",
        "navigation": "cmspage/includes/navigation.html",
        "footer": "cmspage/includes/footer.html",
    }

    settings.CMSPAGE_TEMPLATE_BASE = base_name
    settings.CMSPAGE_TEMPLATE_INCLUDE_FILES = include_names

    # Create a CMSPage instance
    page = CMSPage(title=title, slug=slugify(title))
    page.pk = 1

    # Create a HttpRequest instance
    request = HttpRequest()

    # Call the get_context method
    context = page.get_context(request)

    # Check that the context contains the expected keys
    assert "base_template" in context
    assert "include" in context
    assert "page" in context
    assert "request" in context

    # Check that the context contains the correct values
    assert context["page"] == page
    assert context["request"] == request
    assert context["base_template"] == expected_base
    assert context["include"] == expected_includes

    # Restore original cache state
    functional.cache_state = original_cache_state
