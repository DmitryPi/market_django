from django.test import TestCase

from backend.referrals.tests.factories import ReferralFactory

from .factories import TokenOrderFactory, TokenRoundFactory, UserFactory


class TokenOrderTests(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(username="PARENT")
        self.user_1 = UserFactory(username="CHILD")
        self.referral = ReferralFactory(parent=self.user, child=self.user_1)
        self.token_round = TokenRoundFactory()

    def test_create(self):
        order = TokenOrderFactory(buyer=self.user_1)
        parent = order.buyer.parent
        print(parent)
        print(parent)
        print(parent)
        print(parent)
        # self.assertEqual(order.buyer, self.user)
        # self.assertTrue(order.amount)
