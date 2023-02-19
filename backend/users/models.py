from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "customer"
        SELLER = "SELLER", "seller"

    # Fields
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    type = models.CharField(
        max_length=12, choices=Types.choices, default=Types.CUSTOMER
    )
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.CUSTOMER)
        return queryset


class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=User.Types.SELLER)
        return queryset


class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.CUSTOMER
        self.is_customer = True
        return super().save(*args, **kwargs)


class Seller(User):
    class Meta:
        proxy = True

    objects = SellerManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.SELLER
        self.is_seller = True
        return super().save(*args, **kwargs)
