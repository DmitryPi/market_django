from django.urls import path

from .apps import PagesConfig
from .views import PageDetailView

app_name = PagesConfig.verbose_name

urlpatterns = [
    path("<str:slug>/", PageDetailView.as_view(), name="page-detail"),
]
