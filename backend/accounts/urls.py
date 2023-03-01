from django.urls import path

from .apps import AccountsConfig
from .views import CustomSignupView, CustomSignView

app_name = AccountsConfig.verbose_name
urlpatterns = [
    path("signin/", CustomSignView.as_view(), name="signin"),
    path("signup/", CustomSignupView.as_view(), name="signup"),
]
