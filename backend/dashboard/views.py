from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, View

from .forms import AvatarUpdateForm, CustomUserUpdateForm

User = get_user_model()


class DashboardView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/index.html"


class DashboardSettingsView(SuccessMessageMixin, UpdateView):
    form_class = CustomUserUpdateForm
    template_name = "dashboard/settings.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("board:settings")

    def get_object(self, *args, **kwargs):
        return self.request.user


class AvatarUpdateView(View):
    def post(self, request):
        form = AvatarUpdateForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES:
            user = self.request.user
            user.avatar = form.cleaned_data.get("avatar")
            user.save()
            return JsonResponse({"avatar_url": user.avatar.url})
        # handle form errors
        errors = form.errors.as_data()
        error_messages = [
            error.message for error_list in errors.values() for error in error_list
        ]
        return JsonResponse({"error": error_messages}, status=400)


class DashboardRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("board:index", kwargs={"username": self.request.user.username})
