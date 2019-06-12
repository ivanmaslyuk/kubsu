from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


"""
Формы -- это такие объекты, которые при рендеринге страницы превращаются
в HTML, а затем все, что в ней написал юзер и отправил нам, они представляют
в виде питоновского словаря (грубо говоря), предварительно проверив все
данные на валидность.

В данном случае мы используем формы типа ModelForm, которые просто берут
выбранную нами модель (а модель, по своей сути, является таблицой в БД)
и превращяют их в форму. Кроме того, они сами умеют сохранять данные в БД,
стоит нам их только попросить.
Единственное, что просит нас ModelForm -- это приложить к нашей форме
информацию о том, какую модель использовать, а так же какие и в каком порядке 
отображать поля из данной модели во встроенном классе Meta.

Важно понимать, что формы возвращают только поля. Ни кнопки submit, ни тегов
<form></form> они не предоставляют. Это также значит, что разные Django-формы
можно совмещать в одну HTML-форму.
"""


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'faculty',
            'path',
            'course'
        )

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, label='Имя')
    last_name = forms.CharField(max_length=40, label='Фамилия')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user