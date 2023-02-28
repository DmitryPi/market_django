from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label=_("Имя"),
        widget=TextInput(attrs={"placeholder": _("First Name")}),
    )
    second_name = forms.CharField(
        max_length=30,
        label=_("Фамилия"),
        widget=TextInput(attrs={"placeholder": _("Second Name")}),
    )
    phone_regex = RegexValidator(
        regex=r"^8 \(\d{3}\) \d{3}-\d{2}-\d{2}$",
        message=_("Phone number must be in the format: '8 (999) 999-99-99'."),
    )
    phone_number = forms.CharField(
        max_length=30,
        label=_("Телефон"),
        # validators=[phone_regex],
        widget=TextInput(attrs={"type": "tel", "placeholder": _("8 (999) 999-99-99")}),
    )
    referral = forms.CharField(max_length=30, required=False, label=_("Вас пригласил"))

    field_order = [
        "first_name",
        "second_name",
        "phone_number",
        "email",
        "username",
        "password1",
        "password2",
        "referral",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Email"
        self.fields["email"].required = True
        self.fields["email"].widget.attrs.update({"placeholder": "mail@gmail.com"})

        self.fields["username"].label = "Login"
        self.fields["username"].widget.attrs.update({"placeholder": "Login"})

        self.fields["password1"].label = _("Пароль")
        self.fields["password1"].widget.attrs.update({"placeholder": "*********"})

        self.fields["password2"].label = _("Повторите пароль")
        self.fields["password2"].widget.attrs.update({"placeholder": "*********"})

    def save(self, request):
        user = super().save(request)
        # user_type = self.cleaned_data.get("user_type")

        # if user_type == User.Types.CUSTOMER:
        #     user.is_customer = True
        # elif user_type == User.Types.SELLER:
        #     user.is_seller = True
        # elif user_type == User.Types.BOTH:
        #     user.is_customer = True
        #     user.is_seller = True
        # user.save()

        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
