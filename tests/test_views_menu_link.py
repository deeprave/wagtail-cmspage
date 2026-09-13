from cmspage.views import MenuLinkViewSet


def test_menu_link_list_display_includes_id():
    assert MenuLinkViewSet.list_display[0] == "id"
    assert "id" in MenuLinkViewSet.list_display
