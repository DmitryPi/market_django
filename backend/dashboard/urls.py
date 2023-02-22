from django.urls import path

from .apps import DashboardConfig
from .views import DashboardSettingsView, DashboardView

app_name = DashboardConfig.verbose_name

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("settings/", DashboardSettingsView.as_view(), name="settings"),
]
