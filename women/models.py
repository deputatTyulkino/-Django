from django.db import models
from django.shortcuts import reverse
from taggit.managers import TaggableManager


class PulishedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_published=Women.Status[1])
            .select_related("cat")
        )


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

    cat = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="women")

    objects = models.Manager()
    published = PulishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories", kwargs={"cat_slug": self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
