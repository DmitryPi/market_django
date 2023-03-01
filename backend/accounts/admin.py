from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "avatar")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_customer",
                    "is_seller",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Настройки"),
            {
                "fields": (
                    "email_notifications",
                    "language",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "name",
        "is_superuser",
        "is_customer",
        "is_seller",
    ]
    search_fields = ["name"]
