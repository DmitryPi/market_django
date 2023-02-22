from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, TemplateView

User = get_user_model()


class DashboardView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/index.html"


class DashboardSettingsView(TemplateView):
    template_name = "dashboard/settings.html"


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("board:index", kwargs={"username": self.request.user.username})
