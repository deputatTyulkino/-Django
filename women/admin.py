from uuid import uuid4
from django.contrib import admin
from .models import Women, Category, Husband
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe


# Register your models here.
class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    # request - объект запроса, model_admin - объект модели
    def lookups(self, request, model_admin):
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        else:
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['photo', 'title', 'slug', 'content', 'cat']
    list_display = (
        "title",
        'post_photo',
        "time_create",
        "is_published",
        "information",
    )
    list_dispaly_links = ("title",)
    ordering = (
        "time_create",
        "title",
    )
    list_editable = ("is_published",)
    list_per_page = 3
    search_fields = ("title", "cat__name")
    list_filter = [MarriedFilter, "cat__name", "is_published"]
    prepopulated_fields = {'slug': ['title']}
    # readonly_fields = ['slug']

    actions = ["set_published", "set_draft"]

    def save(self, *args, **kwargs):
      if not self.slug:
        self.slug = slugify(self.title)
        if Women.objects.filter(slug=self.slug).exists():
            self.slug += f"-{uuid4()}"
      super().save(*args, **kwargs)


    @admin.display(description='Фото')
    def post_photo(self, women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50 />")
        return 'Без фото'

    @admin.display(description="Краткое содержание", ordering="content")
    def information(self, women):
        return f"{women.content[:30]}..." if len(women.content) > 30 else women.content

    # request - объект запроса, queryset - список объектов
    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        count = queryset.update(is_publised=Women.Status[1])
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status[0])
        self.message_user(
            request, f"{count} записей снято с публикации", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    prepopulated_fields = {'slug': ('name', )}
    list_display_links = ("name",)


@admin.register(Husband)
class HusbandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "age",
        "m_count",
    )
    list_display_links = ("name",)
