from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import TokenPurchaseManager, TokenRewardManager

User = get_user_model()


class Token(models.Model):
    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    # Relations
    active_round = models.ForeignKey(
        "TokenRound",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("Активный раунд"),
    )
    # Fields
    name = models.CharField(
        _("Название"), unique=True, db_index=True, max_length=50, default="Token"
    )
    total_amount = models.PositiveBigIntegerField(_("Всего токенов"))
    total_amount_sold = models.PositiveBigIntegerField(_("Продано токенов"), default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.active_round.unit_price}"

    @property
    def total_amount_left(self):
        return self.total_amount - self.total_amount_sold


class TokenRound(models.Model):
    class Meta:
        verbose_name = _("Token Round")
        verbose_name_plural = _("Token Rounds")
        ordering = ["unit_price"]

    class Currency(models.TextChoices):
        USD = "$", "USD"

    name = models.CharField(_("Название"), max_length=50, default=_("Раунд"))
    currency = models.CharField(
        _("Валюта"), max_length=5, choices=Currency.choices, default=Currency.USD
    )
    unit_price = models.DecimalField(_("Цена"), max_digits=6, decimal_places=3)
    total_cost = models.PositiveIntegerField(_("Цена за все"))
    total_amount_sold = models.PositiveIntegerField(_("Продано в раунде"), default=0)
    percent_share = models.PositiveSmallIntegerField(_("Доля"))
    is_active = models.BooleanField(_("Активен"), default=False)
    is_complete = models.BooleanField(_("Завершен"), default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.unit_price} - {self.total_cost}"

    def clean(self):
        if self.unit_price <= 0:
            raise ValidationError({"unit_price": _("Price can't be less then 0.")})

    @property
    def progress(self):
        pass


class TokenOrder(models.Model):
    class Meta:
        verbose_name = _("Token Order")
        verbose_name_plural = _("Token Orders")
        ordering = ["-created_at"]

    class Type(models.TextChoices):
        PURCHASE = _("Purchase"), _("Purchase")
        REWARD = _("Reward"), _("Reward")

    # Relations
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Покупатель")
    token_round = models.ForeignKey(
        TokenRound,
        on_delete=models.PROTECT,
        related_name="token_orders",
        verbose_name="Раунд",
    )
    # Fields
    type = models.CharField(
        _("Тип"), max_length=20, choices=Type.choices, default=Type.PURCHASE
    )
    amount = models.PositiveIntegerField(_("Количество"))
    reward = models.PositiveIntegerField(_("Награда"), blank=True, null=True)
    reward_sent = models.BooleanField(_("Награда начислена"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} - {self.amount} - {self.price_sum}"

    def save(self, *args, **kwargs):
        self.reward = self.calc_reward(self.buyer.parent)
        if self.reward:
            self.type = self.Type.REWARD
        return super().save(*args, **kwargs)

    @property
    def price_sum(self):
        return round(self.token_round.unit_price * self.amount, 2)

    def calc_reward(self, parent: User) -> int:
        if parent:
            return round(self.amount * (self.token_round.percent_share / 100))
        return 0


class TokenReward(TokenOrder):
    class Meta:
        proxy = True
        verbose_name = _("Token Reward")
        verbose_name_plural = _("Token Rewards")

    objects = TokenRewardManager()

    def save(self, *args, **kwargs):
        self.type = TokenOrder.Type.REWARD
        return super().save(*args, **kwargs)


class TokenPurchase(TokenOrder):
    class Meta:
        proxy = True
        verbose_name = _("Token Purchase")
        verbose_name_plural = _("Token Purchases")

    objects = TokenPurchaseManager()

    def save(self, *args, **kwargs):
        self.type = TokenOrder.Type.PURCHASE
        return super().save(*args, **kwargs)
