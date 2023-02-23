from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView

from .forms import AvatarUpdateForm

User = get_user_model()


class DashboardView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/index.html"


class DashboardSettingsView(DetailView):
    template_name = "dashboard/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar_form"] = AvatarUpdateForm
        return context

    def get_object(self, *args, **kwargs):
        return self.request.user

    def post(self, request):
        form = AvatarUpdateForm(request.POST, request.FILES)

        if form.is_valid() and request.FILES:
            user = self.request.user
            user.avatar = form.cleaned_data.get("avatar")
            user.save()
            return redirect("board:settings")

        return render(request, "dashboard/settings.html", {"avatar_form": form})


class DashboardRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("board:index", kwargs={"username": self.request.user.username})
