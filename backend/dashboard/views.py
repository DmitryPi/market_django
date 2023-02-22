from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


class DashboardSettingsView(TemplateView):
    template_name = "dashboard/settings.html"
