from django.urls import resolve, reverse

url_prefix = "/board"


def test_dashboard_index():
    rev = reverse("board:index")
    res = resolve(f"{url_prefix}/").view_name
    assert rev == f"{url_prefix}/"
    assert res == "board:index"


def test_dashboard_settings():
    rev = reverse("board:settings")
    res = resolve(f"{url_prefix}/settings/").view_name
    assert rev == f"{url_prefix}/settings/"
    assert res == "board:settings"
