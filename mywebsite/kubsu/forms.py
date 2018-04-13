from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Document


"""
В чем кайф джанго:
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
            'first_name',
            'last_name',
            'father_name',
            'faculty',
            'path',
            'course',
        )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'file',
        )
    
    def save(self, commit=True):
        doc = super(DocumentForm, self).save(commit=False)
        doc.title = self.cleaned_data['file'].name
        if commit:
            doc.save()
        return doc


# Наследуем для формы регистрации от стандартной джанговской формы рег-ции,
# потому что она автоматически дает нам правильные поля для пароля и подтверждения пароля.
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
        )