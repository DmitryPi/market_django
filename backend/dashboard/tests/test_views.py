from django.test import TestCase
from django.urls import reverse

from backend.users.tests.factories import UserFactory


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("board:index")

    def test_response(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")

    def test_response_anon(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class DashboardSettingsViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("board:settings")

    def test_response(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/settings.html")

    def test_response_anon(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
