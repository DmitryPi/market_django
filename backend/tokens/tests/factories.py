from decimal import Decimal

from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from backend.users.tests.factories import UserFactory

from ..models import TokenOrder, TokenRound

fake = Faker()


class TokenRoundFactory(DjangoModelFactory):
    class Meta:
        model = TokenRound

    unit_price = Decimal("0.001")
    percent_share = 5
    total_cost = 0


class TokenOrderFactory(DjangoModelFactory):
    class Meta:
        model = TokenOrder

    buyer = SubFactory(UserFactory)
    token_round = SubFactory(TokenRoundFactory)

    amount = LazyFunction(lambda: fake.random_int(min=100, max=100000))
    reward = LazyFunction(lambda: fake.random_int(min=0, max=1000))
