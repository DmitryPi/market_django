from factory import Faker
from factory.django import DjangoModelFactory

from ..models import Page


class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    title = Faker("word")
    slug = Faker("word")
    content = Faker("paragraph")
