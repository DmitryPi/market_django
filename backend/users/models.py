from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomerManager, SellerManager


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
    phone_number = models.CharField(
        _("Номер телефона"),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?\d{1,3}[\d\s-]{5,}$",
                message='Phone number must be in the format "+999 999-9999".',
            )
        ],
    )
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    metamask_wallet = models.CharField(max_length=155, blank=True)
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
