from django.contrib import admin

from .models import Token, TokenOrder, TokenPurchase, TokenReward, TokenRound


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["name", "total_amount", "total_amount_sold"]


@admin.register(TokenRound)
class TokenRoundAdmin(admin.ModelAdmin):
    list_display = [
        "unit_price",
        "total_cost",
        "percent_share",
        "is_active",
        "is_complete",
    ]


@admin.register(TokenOrder)
class TokenOrderAdmin(admin.ModelAdmin):
    list_display = ["buyer", "type", "amount", "reward", "price_sum"]


@admin.register(TokenPurchase)
class TokenPurchaseAdmin(TokenOrderAdmin):
    pass


@admin.register(TokenReward)
class TokenRewardAdmin(TokenOrderAdmin):
    pass
