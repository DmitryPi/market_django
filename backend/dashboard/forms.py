from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_size(image, max_size: int = 100000):
    if image.size > max_size:
        raise ValidationError(_(f"The maximum image size is {int(max_size / 1000)}kb"))


def validate_image_pixel_size(
    image,
    min_width: int = 100,
    min_height: int = 100,
    max_width: int = 1000,
    max_height: int = 1000,
):
    print(image.size)
    width, height = image.image.size
    if width < min_width or height < min_height:
        raise ValidationError(
            _(f"The minimum image dimensions are {min_width} x {min_height} pixels."),
            code="invalid_pixel_size",
        )
    if width > max_width or height > max_height:
        raise ValidationError(
            _(f"The maximum image dimensions are {max_width} x {max_height} pixels."),
            code="invalid_pixel_size",
        )


class AvatarUpdateForm(forms.Form):
    avatar = forms.ImageField(
        required=False,
        validators=[validate_image_size, validate_image_pixel_size],
    )
