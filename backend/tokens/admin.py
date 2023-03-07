from django.contrib import admin

from .models import Token, TokenPurchase, TokenRound


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
        "is_completed",
    ]


@admin.register(TokenPurchase)
class TokenPurchaseAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "total_cost", "created_at"]
