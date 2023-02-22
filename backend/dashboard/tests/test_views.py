from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def setUp(self):
        pass

    def test_response(self):
        response = self.client.get(reverse("board:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")


class DashboardSettingsViewTests(TestCase):
    def setUp(self):
        pass

    def test_response(self):
        response = self.client.get(reverse("board:settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/settings.html")
