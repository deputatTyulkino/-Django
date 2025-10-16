from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404


# Create your views here.
def index(request):
    data = {'title': 'Главная страница'}
    return render(request, 'base.html', data)

def about(request):
    return render(request, 'about.html')

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat_id}</p>")


def archive(request, year):
    if year > 2025:
        # return redirect('/') врменный редирект
        # return redirect('/', permanent=True) постоянный редирект
        # return redirect(index)
        uri = reverse("categories", args=("music",))
        return redirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
