from factory import SubFactory
from factory.django import DjangoModelFactory

from backend.users.tests.factories import UserFactory

from ..models import Referral


class ReferralFactory(DjangoModelFactory):
    class Meta:
        model = Referral

    parent = SubFactory(UserFactory)
    child = SubFactory(UserFactory)
