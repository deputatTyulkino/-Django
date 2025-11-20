from django import forms
from .models import Category, Husband, Women
from django.core.validators import ValidationError
from captcha.fields import CaptchaField

class AddPageForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='--empty--',
        label='Категория'
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        empty_label='--empty--',
        label='Муж'
    )
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-photo'}))

    class Meta:
        model = Women
        fields = ['photo','title', 'content', 'cat', 'husband']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 4})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class InfForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=12)

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.EmailField(label='Email', max_length=255)
    content = forms.CharField(label='Content', widget=forms.Textarea)
    captcha = CaptchaField()
