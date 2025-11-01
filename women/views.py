from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import Women, Category
from taggit.models import Tag
from .forms import AddPageForm
from django.contrib import messages
import uuid


# Create your views here.
def index(request):
    data = {"title": "Главная страница"}
    return render(request, "base.html", data)


def about(request):
    return render(request, "about.html")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(category_id=category.pk)

    data = {
        "title": category.title,
        "posts": posts,
        "cat_selected": category.pk,
    }

    return render(request, "about.html", data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        "title": post.title,
        "post": post,
    }

    return render(request, "post.html", data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def add_page(request):
    if request.method == "POST":
        form = AddPageForm(request.POST)
        if form.is_valid():
            messages.success("Form add db")
            form.save()
            redirect('home')
    form = AddPageForm()
    return render(request, "addPageForm.html", {"title": "Добавить пост", "form": form})


def contact(request):
    return HttpResponse("Обратная связь")


def show_tag_postlist(request, tag_slug):
    tags = get_object_or_404(Tag, slug=tag_slug)
    category = Category.objects.filter(tags=tags)
    women = category.women.all()

    data = {
        "title": tags.name,
        "posts": women,
        "cat_selected": category.pk,
    }

    return render(request, "about.html", data)
