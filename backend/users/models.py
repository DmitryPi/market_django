from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "customer"
        SELLER = "SELLER", "seller"
        BOTH = "BOTH", "both"

    class Lang(models.TextChoices):
        EN = "EN", "EN"
        RU = "RU", "RU"

    # Fields
    email = models.EmailField(_("Email Address"), blank=True, null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    type = models.CharField(
        max_length=12, choices=Types.choices, default=Types.CUSTOMER
    )
    is_customer = models.BooleanField(_("Покупатель"), default=False)
    is_seller = models.BooleanField(_("Продавец"), default=False)
    # Settings
    email_notifications = models.BooleanField(default=True)
    language = models.CharField(max_length=3, choices=Lang.choices, default=Lang.EN)

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
