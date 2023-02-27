from .models import Page


def pages_qs(request):
    """Expose Pages to global context"""
    pages = Page.objects.all()
    return {"pages": pages}
