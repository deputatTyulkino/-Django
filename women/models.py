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

    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='photos/%Y/%m/%d',
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(
        choices=Status, default=Status[1], verbose_name="Опубликовано"
    )

    husband = models.OneToOneField(
        "Husband",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="women",
        verbose_name="Жених",
    )

    cat = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="women",
        verbose_name="Категория",
    )

    objects = models.Manager()
    published = PulishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories", kwargs={"cat_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Husband(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    age = models.IntegerField(null=True, verbose_name="Возраст")
    m_count = models.IntegerField(
        blank=True, default=0, verbose_name="Количество детей"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жених"
        verbose_name_plural = "Женихи"
