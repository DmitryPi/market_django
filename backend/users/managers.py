from django.contrib.auth.models import BaseUserManager


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
