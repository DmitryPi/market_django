from factory import SubFactory
from factory.django import DjangoModelFactory

from backend.users.tests.factories import UserFactory

from ..models import Referral


class ReferralFactory(DjangoModelFactory):
    class Meta:
        model = Referral

    referrer = SubFactory(UserFactory)
    referred_user = SubFactory(UserFactory)
