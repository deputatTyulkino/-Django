from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import get_user_model

User = get_user_model()

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')
