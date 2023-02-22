from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


class DashboardSettingsView(TemplateView):
    template_name = "dashboard/settings.html"


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("board:index")
