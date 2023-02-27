from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and "accounts" not in request.path
            and "pages" not in request.path
        ):
            return redirect(reverse("account_login"))
        response = self.get_response(request)
        return response
