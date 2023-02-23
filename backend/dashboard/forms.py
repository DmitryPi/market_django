from django import forms

from .validators import (
    validate_image_max_pixel_size,
    validate_image_min_pixel_size,
    validate_image_size,
)


class AvatarUpdateForm(forms.Form):
    avatar = forms.ImageField(
        required=False,
        validators=[
            validate_image_size,
            validate_image_min_pixel_size,
            validate_image_max_pixel_size,
        ],
    )
