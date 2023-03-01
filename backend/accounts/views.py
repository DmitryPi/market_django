from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from eth_account.messages import defunct_hash_message
from web3.auto import w3

User = get_user_model()


def metamask_login(request):
    if request.method == "POST":
        public_address = request.POST["accountAddress"]
        signature = request.POST["signature"]
        csrf_token = request.POST["csrfmiddlewaretoken"]

        original_message = f"Sign in to our website {csrf_token}"
        message_hash = defunct_hash_message(text=original_message)
        signer = w3.eth.account.recoverHash(message_hash, signature=signature)

        if signer == public_address:
            user = User.objects.filter(metamask_wallet=public_address).first()
            if user:
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return HttpResponseRedirect(
                    reverse("dashboard:index", kwargs={"username": user.username})
                )
            messages.add_message(request, messages.WARNING, _("Пользователь не найден"))
        else:
            messages.add_message(
                request, messages.WARNING, _("Обновите страницу и попробуйте еще раз")
            )
    return HttpResponseRedirect(reverse("accounts:signin"))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self, *args, **kwargs):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
