from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "customer"
        SELLER = "SELLER", "seller"
        BOTH = "BOTH", "both"

    # Fields
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    type = models.CharField(
        max_length=12, choices=Types.choices, default=Types.CUSTOMER
    )
    is_customer = models.BooleanField(_("Покупатель"), default=False)
    is_seller = models.BooleanField(_("Продавец"), default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_customer=True)
        return queryset


class SellerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_seller=True)
        return queryset


class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
            self.is_customer = True
        return super().save(*args, **kwargs)


class Seller(User):
    class Meta:
        proxy = True

    objects = SellerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CUSTOMER
            self.is_seller = True
        return super().save(*args, **kwargs)
