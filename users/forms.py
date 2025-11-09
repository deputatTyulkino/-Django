from django import forms
from django.contrib.auth.forms import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

User = get_user_model()

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password1')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользовать с таким email уже существует')

        return email

    # Или в представлениях прописать 2 строчки хеширования пароля
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Email', disabled=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', max_length=30, widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New password', max_length=30, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='New password again', max_length=30, widget=forms.PasswordInput)
