from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from .factories import Referral, ReferralFactory, UserFactory


class ReferralTests(TestCase):
    def setUp(self) -> None:
        self.batch_size = 5
        self.user = UserFactory(username="test")
        self.user_1 = UserFactory(username="test1")

    def test_create(self):
        ReferralFactory.create_batch(self.batch_size, referrer=self.user)
        self.assertEqual(Referral.objects.count(), self.batch_size)

    def test_delete(self):
        referral = ReferralFactory()
        referral.delete()
        self.assertEqual(Referral.objects.count(), 0)

    def test_delete_cascade(self):
        ReferralFactory(referrer=self.user, referred_user=self.user_1)
        self.user.delete()
        self.user_1.refresh_from_db()
        self.assertFalse(Referral.objects.count())
        self.assertTrue(self.user_1)

    def test_fields(self):
        referral = ReferralFactory()
        self.assertTrue(referral.referrer)
        self.assertTrue(referral.referred_user)
        self.assertTrue(referral.created_at)

    def test_str(self):
        referral = ReferralFactory()
        self.assertEqual(
            str(referral),
            f"{referral.referrer.username} referrer of {referral.referred_user.username}",
        )

    def test_clean_referrer_not_equal_referred_user(self):
        referral = Referral(
            referrer=self.user,
            referred_user=self.user,
        )
        # Ensure the clean method raises a validation error
        with self.assertRaises(ValidationError):
            referral.clean()

    def test_clean_unique(self):
        referral = ReferralFactory()
        existing_referral = Referral(
            referrer=referral.referrer,
            referred_user=referral.referred_user,
        )
        # Ensure the clean method raises a validation error
        with self.assertRaises(ValidationError):
            existing_referral.clean()

    def test_unique_constraint_for_referred_user(self):
        new_user = UserFactory()
        ReferralFactory(
            referred_user=self.user,
            referrer=new_user,
        )
        # Ensure the unique constraint is enforced
        with self.assertRaises(IntegrityError):
            ReferralFactory(
                referred_user=self.user,
                referrer=new_user,
            )
