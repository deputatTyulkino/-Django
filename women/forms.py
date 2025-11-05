from django import forms
from .models import Category, Husband, Women
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError
from string import ascii_letters, digits
from django.utils.deconstruct import deconstructible

# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = ascii_letters + '0123456789'
#     code = 'russian'

#     def __init__(self, message=None):
#         self.message = message if message else 'Только русские символы, дефис и пробел'

#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


# class AddPageForm(forms.Form):
#     title = forms.CharField(
#         max_length=255,
#         min_length=3,
#         label='Заголовок',
#         # validators=[RussianValidator()]
#         error_messages={
#             'min_length': 'Слишком короткий заголовок',
#             'required': 'Без заголовка нельзя'
#         }
#     )
#     slug = forms.SlugField(max_length=255, label='URL', validators=[
#         MinLengthValidator(5, message='Минимум 5 символов'),
#         MaxLengthValidator(100, message='Максимум 100 символов')
#     ])
#     email = forms.EmailField(max_length=100, label='Email')
#     content = forms.CharField(widget=forms.Textarea, label='Контент')
#     is_published = forms.BooleanField(label='Статус')
#     cat = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         empty_label='--empty--',
#         label='Категория'
#     )
#     husband = forms.ModelChoiceField(
#         queryset=Husband.objects.all(),
#         empty_label='--empty--',
#         label='Муж'
#     )

#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = ascii_letters + '0123456789'
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError('Только русские символы, дефис и пробел')

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
        # labels = {
        #     'title': 'Не имя'
        # }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

class InfForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=12)
