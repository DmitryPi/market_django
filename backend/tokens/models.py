from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Token(models.Model):
    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    # Relations
    active_round = models.ForeignKey(
        "TokenRound", on_delete=models.PROTECT, related_name="+"
    )
    # Fields
    name = models.CharField(
        _("Название"), unique=True, db_index=True, max_length=50, default="Token"
    )
    total_amount = models.PositiveIntegerField(_("Осталось токенов"))
    total_sold = models.PositiveIntegerField(_("Продано токенов"), default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.active_round.unit_price}"

    @property
    def total_amount_left(self):
        return self.total_amount - self.total_sold


class TokenRound(models.Model):
    class Meta:
        verbose_name = _("Token Round")
        verbose_name_plural = _("Token Rounds")
        ordering = ["unit_price"]

    class Currency(models.TextChoices):
        USD = "$", "USD"

    currency = models.CharField(
        _("Валюта"), max_length=5, choices=Currency.choices, default=Currency.USD
    )
    unit_price = models.DecimalField(_("Цена"), max_digits=6, decimal_places=3)
    total_cost = models.PositiveIntegerField(_("Цена за все"))
    percent_share = models.PositiveSmallIntegerField(_("Доля"))
    is_active = models.BooleanField(_("Активен"), default=False)
    is_completed = models.BooleanField(_("Завершен"), default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.unit_price} - {self.total_cost}"

    def clean(self):
        if self.unit_price <= 0:
            raise ValidationError({"unit_price": _("Price can't be less then 0.")})

    @property
    def progress_percent(self):
        pass


class TokenPurchase(models.Model):
    class Meta:
        verbose_name = _("Token Purchase")
        verbose_name_plural = _("Token Purchases")
        ordering = ["-created_at"]

    # Relations
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # Fields
    amount = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.total_cost}"
