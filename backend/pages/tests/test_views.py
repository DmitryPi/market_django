from django.test import TestCase
from django.urls import reverse

from .factories import PageFactory

# class AboutViewTests(TestCase):
#     def setUp(self):
#         self.url = reverse("pages:about")

#     def test_get(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "pages/about.html")


class PageDetailView(TestCase):
    def setUp(self):
        self.page_1 = PageFactory(title="About")
        self.page_2 = PageFactory(title="Policy")
        self.url_1 = reverse("pages:page-detail", kwargs={"slug": self.page_1.slug})
        self.url_2 = reverse("pages:page-detail", kwargs={"slug": self.page_2.slug})

    def test_get(self):
        response = self.client.get(self.url_1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/detail.html")
        self.assertContains(response, self.page_1.title)
