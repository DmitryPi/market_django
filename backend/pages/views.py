from django.views.generic import DetailView

from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/detail.html"
    slug_url_kwarg = "slug"
