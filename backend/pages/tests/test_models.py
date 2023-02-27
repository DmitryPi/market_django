from django.test import TestCase

from .factories import Page, PageFactory


class PageTests(TestCase):
    def setUp(self):
        self.batch_size = 5
        self.pages = PageFactory.create_batch(self.batch_size)

    def test_create(self):
        self.assertEqual(Page.objects.count(), self.batch_size)

    def test_update(self):
        new_title = "new title"
        for obj in self.pages:
            obj.title = new_title
            obj.save()
        for obj in self.pages:
            self.assertEqual(obj.title, new_title)

    def test_delete(self):
        for obj in self.pages:
            obj.delete()
        self.assertEqual(Page.objects.count(), 0)

    def test_fields(self):
        for obj in self.pages:
            self.assertTrue(obj.title)
            self.assertTrue(obj.slug)
            self.assertTrue(obj.content)
            self.assertTrue(obj.updated_at)
            self.assertTrue(obj.created_at)
