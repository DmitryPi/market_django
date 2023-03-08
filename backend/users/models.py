from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_phone_number


class User(AbstractUser):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )
    phone_number = models.CharField(
        _("Номер телефона"),
        max_length=30,
        blank=True,
        validators=[validate_phone_number],
    )
    date_of_birth = models.DateField(_("Дата рождения"), blank=True, null=True)
    city = models.CharField(_("Город"), max_length=50, blank=True)
    avatar = models.ImageField(
        _("Аватар"), upload_to="avatars/", default="avatars/default.png"
    )
    metamask_wallet = models.CharField(_("Metamask"), max_length=155, blank=True)

    def get_absolute_url(self):
        return reverse("dashboard:index", kwargs={"username": self.username})

    def clean(self):
        if self.parent == self:
            raise ValidationError({"parent": _("Parent and Child cannot be the same.")})
