from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .forms import ProfileUserForm, UserPasswordChangeForm

User = get_user_model()

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('home')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': '...'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
