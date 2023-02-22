from django.urls import path

from .apps import DashboardConfig
from .views import DashboardRedirectView, DashboardSettingsView, DashboardView

app_name = DashboardConfig.verbose_name

urlpatterns = [
    path("~redirect/", view=DashboardRedirectView.as_view(), name="redirect"),
    path("~settings/", DashboardSettingsView.as_view(), name="settings"),
    path("<str:username>/", DashboardView.as_view(), name="index"),
]
