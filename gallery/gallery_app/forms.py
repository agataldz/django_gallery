from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from gallery_app.models import Photo, Comment


class AddUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Podane hasła nie są identyczne")
        return cleaned_data


class AddPhotoForm(forms.ModelForm):
    class Meta:

        model = Photo
        exclude = ['username']
        labels = {
            "photo": "Wybierz zdjęcie",
            "title": "Tytuł",
            "description": "Opis"
        }


class AddCommentForm(forms.ModelForm):
    class Meta:

        model = Comment
        exclude = ['username', 'photo']


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)


class SearchForm(forms.Form):
    key = forms.CharField(label='Wyszukaj', max_length=64)


class ImageFilterForm(forms.Form):
    CHOICES = (
        ('blur', 'Blur'),
        ('edges', 'Edges'),
        ('modefilter', 'ModeFilter'),
        ('contour', 'Contour'),
        ('sharpen', 'Sharpen'),
    )
    select = forms.CharField(label='Wybierz filtr', widget=forms.Select(choices=CHOICES))


class TextForm(forms.Form):
    CHOICES = (
        ('black', 'Black'),
        ('red', 'Red'),
        ('white', 'White'),
        ('blue', 'Blue')
    )
    select = forms.CharField(label='Wybierz kolor', widget=forms.Select(choices=CHOICES))
    text = forms.CharField(label='Tekst', max_length=32)
