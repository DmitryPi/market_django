from datetime import date

from django.test import TestCase

from backend.users.tests.factories import UserFactory

from ..forms import CustomUserUpdateForm


class CustomUserUpdateFormTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_valid_data(self):
        form = CustomUserUpdateForm(
            data={
                "name": "Test User",
                "email": "testuser@example.com",
                "phone_number": "1234567890",
                "date_of_birth": "1990-01-01",
                "city": "Test City",
                "metamask_wallet": "0x1234567890",
                "password": "newpass123",
                "password1": "newpass123",
            },
            instance=self.user,
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertEqual(user.date_of_birth, date(1990, 1, 1))
        self.assertEqual(user.city, "Test City")
        self.assertEqual(user.metamask_wallet, "0x1234567890")
        self.assertTrue(user.check_password("newpass123"))

    def test_password_mismatch(self):
        form = CustomUserUpdateForm(
            data={
                "name": "Test User",
                "email": "testuser@example.com",
                "phone_number": "1234567890",
                "date_of_birth": "1990-01-01",
                "city": "Test City",
                "metamask_wallet": "0x1234567890",
                "password": "newpass123",
                "password1": "mismatch",
            },
            instance=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_weak_password(self):
        form = CustomUserUpdateForm(
            data={
                "name": "Test User",
                "email": "testuser@example.com",
                "phone_number": "1234567890",
                "date_of_birth": "1990-01-01",
                "city": "Test City",
                "metamask_wallet": "0x1234567890",
                "password": "password",
                "password1": "password",
            },
            instance=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
