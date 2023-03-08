from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Referral(models.Model):
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="parent",
    )
    child = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="child",
        unique=True,
    )

    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")

    def __str__(self) -> str:
        return f"[{self.parent.username}] is a parent of [{self.child.username}]"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def clean(self):
        # Check if referrer refers to himself
        if self.parent == self.child:
            raise ValidationError({"child": _("Parent and Child cannot be the same.")})
        # Check if referral link already exists
        existing_referral = Referral.objects.filter(
            parent=self.parent, child=self.child
        ).first()
        if existing_referral:
            raise ValidationError({"child": _("This referral already exists.")})
