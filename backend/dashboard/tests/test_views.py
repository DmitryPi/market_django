from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from backend.users.tests.factories import UserFactory


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("board:index", kwargs={"username": self.user.username})

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")

    def test_get_anon(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class DashboardSettingsViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("board:settings")

    def test_get(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/settings.html")

    def test_get_anon(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_avatar_form(self):
        self.client.force_login(self.user)
        # read mock image
        with open("backend/dashboard/tests/test_avatar.jpg", "rb") as f:
            image = SimpleUploadedFile(
                "test_avatar.jpg", f.read(), content_type="image/jpeg"
            )
        data = {"avatar": image}
        response = self.client.post(reverse("dashboard:settings"), data, follow=True)
        self.user.refresh_from_db()
        # tests
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/settings.html")
        self.assertIn("avatar_form", response.context)
        self.assertEqual(self.user.avatar, "avatars/test_avatar.jpg")

    def test_post_avatar_form_invalid(self):
        self.client.force_login(self.user)
        # read mock image
        data = {"avatar": ""}
        response = self.client.post(reverse("dashboard:settings"), data, follow=True)
        self.user.refresh_from_db()
        # tests
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/settings.html")
        self.assertIn("avatar_form", response.context)
        self.assertEqual(self.user.avatar, "avatars/default.png")

    def test_post_avatar_form_anon(self):
        data = {"avatar": ""}
        response = self.client.post(reverse("dashboard:settings"), data, follow=True)
        # tests
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")
