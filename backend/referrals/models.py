from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Referral(models.Model):
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referral_links",
    )
    referred_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="referred_by",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")

    def __str__(self) -> str:
        return f"{self.referred_user.username} referred to {self.referrer.username}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def clean(self):
        # Check if referrer refers to himself
        if self.referred_user == self.referrer:
            raise ValidationError(_("Referrer and referred user cannot be the same."))
        # Check if referral link already exists
        existing_referral = Referral.objects.filter(
            referrer=self.referrer, referred_user=self.referred_user
        ).first()
        if existing_referral and existing_referral != self:
            raise ValidationError(_("This referral already exists."))
