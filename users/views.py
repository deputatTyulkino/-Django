from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginUserForm
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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
