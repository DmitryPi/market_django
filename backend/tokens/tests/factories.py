from decimal import Decimal

import factory
from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from backend.users.tests.factories import UserFactory

from ..models import Token, TokenOrder, TokenRound

fake = Faker()


class TokenRoundFactory(DjangoModelFactory):
    class Meta:
        model = TokenRound

    unit_price = Decimal("0.001")
    percent_share = 5
    total_cost = Decimal("10")


class TokenOrderFactory(DjangoModelFactory):
    class Meta:
        model = TokenOrder

    buyer = SubFactory(UserFactory)
    token_round = SubFactory(TokenRoundFactory)

    amount = LazyFunction(lambda: fake.random_int(min=100, max=100000))
    reward = LazyFunction(lambda: fake.random_int(min=0, max=1000))


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token

    active_round = SubFactory(TokenRoundFactory)
    name = factory.Faker("city")
    total_amount = LazyFunction(lambda: fake.random_int(min=100, max=100000000))
    total_amount_sold = LazyFunction(lambda: fake.random_int(min=100, max=100000000))
