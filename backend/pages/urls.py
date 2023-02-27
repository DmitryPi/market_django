from django.urls import path

from .apps import PagesConfig
from .views import AboutView, PolicyView

app_name = PagesConfig.verbose_name

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("policy/", PolicyView.as_view(), name="policy"),
]
