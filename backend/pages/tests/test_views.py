from django.test import TestCase
from django.urls import reverse


class AboutViewTests(TestCase):
    def setUp(self):
        self.url = reverse("pages:about")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")


class PolicyViewTests(TestCase):
    def setUp(self):
        self.url = reverse("pages:policy")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/policy.html")
