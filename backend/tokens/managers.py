from django.db import models


class TokenPurchaseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        from .models import TokenOrder

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=TokenOrder.Type.PURCHASE)
        return queryset


class TokenRewardManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        from .models import TokenOrder

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=TokenOrder.Type.REWARD)
        return queryset
