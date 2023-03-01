import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..forms import UserAdminChangeForm
from ..models import User
from ..views import UserRedirectView, UserUpdateView, user_detail_view
from .factories import UserFactory

pytestmark = pytest.mark.django_db


class MetamaskLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(
            username="testuser",
            metamask_wallet="0xEFE417C9e02f8B36f7969af9e4c40a25Bed74ecF",
        )
        self.url = reverse("metamask_login")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("accounts:signin"))

    # def test_valid_login(self):
    #     signature = "0xabcd1234"
    #     csrf_token = self.client.get(self.url).cookies.get("csrftoken")
    #     data = {
    #         "accountAddress": "0x1234567890abcdef",
    #         "signature": signature,
    #         "csrfmiddlewaretoken": "14124",
    #     }
    #     response = self.client.post(self.url, data=data)
    #     self.assertRedirects(
    #         response, reverse("dashboard:index", kwargs={"username": self.user.username})
    #     )

    def test_invalid_login(self):
        pass


class TestUserUpdateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        form = UserAdminChangeForm()
        form.cleaned_data = {}
        form.instance = user
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Information successfully updated"]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"
