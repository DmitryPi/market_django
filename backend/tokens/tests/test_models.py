from django.test import TestCase

from .factories import TokenOrderFactory, TokenRoundFactory, UserFactory


class TokenOrderTests(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(username="PARENT")
        self.user_1 = UserFactory(username="CHILD", parent=self.user)
        self.user_2 = UserFactory(username="CHILD 2", parent=self.user)
        self.token_round = TokenRoundFactory()

    def test_create(self):
        order = TokenOrderFactory(buyer=self.user_1)
        parent = order.buyer.parent
        print(parent)
        print(self.user.children.all())
        # self.assertEqual(order.buyer, self.user)
        # self.assertTrue(order.amount)
