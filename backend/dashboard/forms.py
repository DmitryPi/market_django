from django import forms
from django.contrib.auth import get_user_model

from .validators import (
    validate_image_max_pixel_size,
    validate_image_min_pixel_size,
    validate_image_size,
)

User = get_user_model()


class AvatarUpdateForm(forms.Form):
    avatar = forms.ImageField(
        required=False,
        validators=[
            validate_image_size,
            validate_image_min_pixel_size,
            validate_image_max_pixel_size,
        ],
    )


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone_number",
            "date_of_birth",
            "city",
            "metamask_wallet",
        ]
