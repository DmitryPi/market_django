from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import (
    Token,
    TokenFactory,
    TokenOrder,
    TokenOrderFactory,
    TokenRound,
    TokenRoundFactory,
    UserFactory,
)


class TokenTests(TestCase):
    def setUp(self) -> None:
        self.batch_size = 5

    def test_create(self):
        TokenFactory.create_batch(self.batch_size)
        self.assertEqual(Token.objects.count(), 5)

    def test_update(self):
        token = TokenFactory()
        token.name = "Test"
        token.amount = 100
        token.save()
        token.refresh_from_db()
        # Tests
        self.assertEqual(token.name, "Test")
        self.assertEqual(token.amount, 100)

    def test_delete(self):
        token = TokenFactory()
        token.delete()
        self.assertFalse(Token.objects.count())

    def test_fields(self):
        token = TokenFactory()
        self.assertTrue(token.active_round)
        self.assertTrue(token.name)
        self.assertTrue(token.total_amount)
        self.assertTrue(token.total_amount_sold)
        self.assertTrue(token.updated_at)

    def test_str(self):
        token = TokenFactory()
        self.assertEqual(str(token), f"{token.name} - {token.active_round.unit_price}")

    def test_total_amount_left(self):
        token = TokenFactory()
        result = token.total_amount - token.total_amount_sold
        self.assertEqual(result, token.total_amount_left)


class TokenRoundTests(TestCase):
    def setUp(self) -> None:
        self.batch_size = 5

    def test_create(self):
        TokenRoundFactory.create_batch(self.batch_size)
        self.assertEqual(TokenRound.objects.count(), 5)

    def test_update(self):
        new_price = Decimal("0.01")
        token_round = TokenRoundFactory()
        token_round.unit_price = new_price
        token_round.save()
        token_round.refresh_from_db()
        # Tests
        self.assertEqual(token_round.unit_price, new_price)

    def test_delete(self):
        token_round = TokenRoundFactory()
        token_round.delete()
        self.assertFalse(TokenRound.objects.count())

    def test_fields(self):
        token_round = TokenRoundFactory()
        self.assertEqual(token_round.name, "Раунд")
        self.assertEqual(token_round.currency, "$")
        self.assertTrue(token_round.unit_price)
        self.assertTrue(token_round.total_cost)
        self.assertEqual(token_round.total_amount_sold, 0)
        self.assertTrue(token_round.percent_share)
        self.assertFalse(token_round.is_active)
        self.assertFalse(token_round.is_complete)
        self.assertTrue(token_round.updated_at)

    def test_clean(self):
        token_round = TokenRoundFactory(unit_price=0)
        with self.assertRaises(ValidationError):
            token_round.clean()

    def test_str(self):
        token_round = TokenRoundFactory()
        self.assertEqual(
            str(token_round), f"{token_round.unit_price} - {token_round.total_cost}"
        )


class TokenOrderTests(TestCase):
    def setUp(self) -> None:
        self.batch_size = 5
        self.user = UserFactory(username="PARENT")
        self.user_1 = UserFactory(username="CHILD", parent=self.user)
        self.user_2 = UserFactory(username="CHILD 2", parent=self.user)
        self.token_round = TokenRoundFactory(unit_price=Decimal("0.1"))

    def test_create(self):
        TokenOrderFactory.create_batch(self.batch_size)
        self.assertEqual(TokenOrder.objects.count(), 5)

    def test_update(self):
        new_amount = 100
        token_order = TokenOrderFactory()
        token_order.amount = 100
        token_order.save()
        token_order.refresh_from_db()
        # Tests
        self.assertEqual(token_order.amount, new_amount)

    def test_delete(self):
        token_order = TokenOrderFactory()
        token_order.delete()
        self.assertFalse(TokenOrder.objects.count())

    def test_fields(self):
        token_order = TokenOrderFactory(buyer=self.user, token_round=self.token_round)
        self.assertEqual(token_order.buyer, self.user)
        self.assertEqual(token_order.token_round, self.token_round)
        self.assertEqual(token_order.type, TokenOrder.Type.PURCHASE)
        self.assertTrue(token_order.amount)
        self.assertFalse(token_order.reward)
        self.assertTrue(token_order.created_at)

    def test_str(self):
        token_order = TokenOrderFactory()
        self.assertEqual(
            str(token_order),
            f"{token_order.buyer.username} - {token_order.amount} - {token_order.price_sum}",
        )

    def test_save(self):
        token_order = TokenOrderFactory()
        # Test default
        self.assertFalse(token_order.reward)
        self.assertEqual(token_order.type, TokenOrder.Type.PURCHASE)
        # Test updated
        token_order.buyer = self.user_1  # user with parent
        token_order.save()
        self.assertTrue(token_order.reward)
        self.assertEqual(token_order.type, TokenOrder.Type.REWARD)

    def test_price_sum(self):
        new_amount = 100
        token_order = TokenOrderFactory(token_round=self.token_round, amount=new_amount)
        self.assertEqual(
            self.token_round.unit_price * new_amount, token_order.price_sum
        )

    def test_calc_reward(self):
        """TODO: more cases"""
        new_amount = 100
        token_round = TokenRoundFactory(unit_price=Decimal("0.1"), percent_share=10)
        token_order = TokenOrderFactory(
            buyer=self.user_1, token_round=token_round, amount=new_amount
        )
        result = token_order.calc_reward(token_order.buyer.parent)
        self.assertEqual(round(new_amount * (token_round.percent_share / 100)), result)

    def test_calc_reward_zero(self):
        new_amount = 100
        token_round = TokenRoundFactory(unit_price=Decimal("0.1"), percent_share=10)
        token_order = TokenOrderFactory(
            buyer=self.user, token_round=token_round, amount=new_amount
        )
        result = token_order.calc_reward(token_order.buyer.parent)
        self.assertEqual(result, 0)
