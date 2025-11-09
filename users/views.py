from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.
# def login(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('home')
#     form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

# def logout(request):
#     logout(request)
#     return redirect('users:login')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             # Либо в форме определить метод save()
#             # user.set_password(form.cleaned_data['password'])
#             # user.save()
#             login(request, user)
#             return redirect('home')
#     form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('home')
