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
        ReferralFactory.create_batch(self.batch_size, parent=self.user)
        self.assertEqual(Referral.objects.count(), self.batch_size)

    def test_delete(self):
        referral = ReferralFactory()
        referral.delete()
        self.assertEqual(Referral.objects.count(), 0)

    def test_delete_cascade(self):
        ReferralFactory(parent=self.user, child=self.user_1)
        self.user.delete()
        self.user_1.refresh_from_db()
        self.assertFalse(Referral.objects.count())
        self.assertTrue(self.user_1)

    def test_fields(self):
        referral = ReferralFactory()
        self.assertTrue(referral.parent)
        self.assertTrue(referral.child)

    def test_str(self):
        referral = ReferralFactory()
        self.assertEqual(
            str(referral),
            f"[{referral.parent.username}] is a parent of [{referral.child.username}]",
        )

    def test_clean_parent_not_equal_child(self):
        referral = Referral(
            parent=self.user,
            child=self.user,
        )
        # Ensure the clean method raises a validation error
        with self.assertRaises(ValidationError):
            referral.clean()

    def test_clean_unique(self):
        referral = ReferralFactory()
        existing_referral = Referral(
            parent=referral.parent,
            child=referral.child,
        )
        # Ensure the clean method raises a validation error
        with self.assertRaises(ValidationError):
            existing_referral.clean()

    def test_unique_constraint_for_child(self):
        new_user = UserFactory()
        ReferralFactory(
            child=self.user,
            parent=new_user,
        )
        # Ensure the unique constraint is enforced
        with self.assertRaises(IntegrityError):
            ReferralFactory(
                child=self.user,
                parent=new_user,
            )
