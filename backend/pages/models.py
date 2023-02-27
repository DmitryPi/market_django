from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True, unique=True, max_length=110)
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:page-detail", kwargs={"slug": self.slug})
