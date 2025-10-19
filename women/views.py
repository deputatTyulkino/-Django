from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Women


# Create your views here.
def index(request):
    data = {'title': 'Главная страница'}
    return render(request, 'base.html', data)

def about(request):
    return render(request, 'about.html')

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat_id}</p>")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    
    data = {
        'title': post.title,
        'post': post,
    }
    
    return render(request, 'post.html', data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def add_page(request):
    return HttpResponse('Добавление статьи')

def contact(request):
    return HttpResponse('Обратная связь')

