from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('home')
    form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('users:login')
