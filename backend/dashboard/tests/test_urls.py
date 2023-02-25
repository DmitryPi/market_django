from django.urls import resolve, reverse

from backend.users.models import User

url_prefix = "/board"


def test_dashboard_index(user: User):
    rev = reverse("board:index", kwargs={"username": user.username})
    res = resolve(f"{url_prefix}/{user.username}/").view_name
    assert rev == f"{url_prefix}/{user.username}/"
    assert res == "board:index"


def test_dashboard_settings():
    rev = reverse("board:settings")
    res = resolve(f"{url_prefix}/~settings/").view_name
    assert rev == f"{url_prefix}/~settings/"
    assert res == "board:settings"


def test_dashboard_settings_avatar_update():
    rev = reverse("board:settings_avatar_update")
    res = resolve(f"{url_prefix}/~settings/avatar-update/").view_name
    assert rev == f"{url_prefix}/~settings/avatar-update/"
    assert res == "board:settings_avatar_update"


def test_redirect():
    assert reverse("board:redirect") == "/board/~redirect/"
    assert resolve("/board/~redirect/").view_name == "board:redirect"
