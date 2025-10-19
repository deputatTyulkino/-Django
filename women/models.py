from django.db import models
from django.shortcuts import reverse


class PulishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status[1])


# Create your models here.
class Women(models.Model):
    Status = (
        ("0", "Черновик"),
        ("1", "Опубликовано"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status, default=Status[1])

    objects = models.Manager()
    published = PulishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]
