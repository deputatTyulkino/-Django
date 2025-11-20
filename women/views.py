from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Women, Category
from taggit.models import Tag
from .forms import AddPageForm, InfForm, ContactForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from .utils import DataMixin
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
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
    current = paginator.get_page(page_number)

    return render(request, 'about.html', {'current': current})

class ShowCategory(ListView):
    template_name = 'about.html'
    context_object_name = 'posts'
    
    def get_category(self, slug):
        return get_object_or_404(Category, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_contet_data(**kwargs)
        context['title'] = self.get_category(self.kwargs['cat_slug']).title
        context['cat_selected'] = self.get_category(self.kwargs['cat_slug']).pk
        return context
    
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Women.published.filter(category_id=category.pk)
        


class PostDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = Women
    template_name = 'post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Women
    fields = '__all__'
    template_name = 'addPageForm.html'
    permission_required = 'women.add_women' # приложение.разрешение_таблица

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin, UpdateView):
    model = Women
    fields = '__all__'
    template_name = 'AddPageForm.html'
    success_url = reverse_lazy('home')
    permission_required = 'women.change_women' # приложение.разрешение_таблица


# @permission_required(perm='women.view_women', raise_exception=True)
# def contact(request):
#     return HttpResponse("Обратная связь")

class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class TagsPostList(DataMixin, ListView):
    template_name = 'about.html'
    context_object_name = 'categories'
    title_page = 'Main Page'
    cat_id = 0
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        tags = Tag.objects.filter(slug=self.kwargs['tag_slug'])
        return Category.objects.filter(tags=tags)

class FormPage(FormView):
    form_class = InfForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

