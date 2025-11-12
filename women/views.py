from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import Women, Category
from taggit.models import Tag
from .forms import AddPageForm, InfForm
from django.contrib import messages
import uuid
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .utils import DataMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def index(request):
    data = {"title": "Главная страница"}
    return render(request, "base.html", data)

@login_required(login_url='/admin/')
def about(request):
    womens = Women.published.all()
    paginator = Paginator(womens, 3)

    page_number = request.GET.get('page')
    current = Paginator.get_page(page_number)

    return render(request, 'about.html', {'current': current})

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(category_id=category.pk)

    data = {
        "title": category.title,
        "posts": posts,
        "cat_selected": category.pk,
    }

    return render(request, "about.html", data)

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)

#     data = {
#         "title": post.title,
#         "post": post,
#     }

#     return render(request, "post.html", data)

class PostDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = Women
    template_name = 'post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'
    # login_url = ...
    # pk_url_kwarg = '...'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def add_page(request):
#     if request.method == "POST":
#         form = AddPageForm(request.POST)
#         if form.is_valid():
#             messages.success("Form add db")
#             form.save()
#             redirect('home')
#     form = AddPageForm()
#     return render(request, "addPageForm.html", {"title": "Добавить пост", "form": form})

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # form_class = AddPageForm
    model = Women
    fields = '__all__'
    template_name = 'addPageForm.html'
    permission_required = 'women.add_women' # приложение.разрешение_таблица
    # success_url = reverse_lazy('home')
    # extra_context = {...}

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


# class AddPage(View):
#     def get(self, request):
#         form = AddPageForm()
#         return render(request, "addPageForm.html", {"title": "Добавить пост", "form": form})

#     def post(self, request):
#         form = AddPageForm(request.POST, request.FILES)
#         if form.is_valid():
#             messages.success("Form add db")
#             form.save()
#             return redirect('home')
#         return render(request, "addPageForm.html", {"title": "Добавить пост", "form": form})

class UpdatePage(PermissionRequiredMixin, UpdateView):
    model = Women
    fields = '__all__'
    template_name = 'AddPageForm.html'
    success_url = reverse_lazy('home')
    permission_required = 'women.change_women' # приложение.разрешение_таблица


@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")

class TagsPostList(DataMixin, ListView):
    template_name = 'about.html'
    # model = Category
    # queryset = Category.objects.filter(...)

    context_object_name = 'categories'
    title_page = 'Main Page'
    cat_id = 0
    # extra_context = {
    #     'title': 'Main page'
    # }
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        tags = Tag.objects.filter(slug=self.kwargs['tag_slug'])
        return Category.objects.filter(tags=tags)

class FormPage(FormView):
    form_class = InfForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    # def get_success_url(self):
    #     return reverse(...)

    # def form_valid(self, form):
    #     ...
    #     return super().form_valid(form)
