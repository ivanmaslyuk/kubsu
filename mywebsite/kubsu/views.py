from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import UserForm, ProfileForm


def index(request):
    return HttpResponse('hello world')


def register(request):
    # Если для открытия страницы использовался метод post,
    # значит нужно обработать данные для регистрации.
    if request.method == 'POST':
        # Создаем экземпляры форм и заполняем их полученной информацией.
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        # Если все данные в формах валидны (ни в одном поле нет недопустимых значений,
        # например, уже существующее имя пользователя или слишком короткий пароль),
        # то начинаем обработку данных.
        if user_form.is_valid() and profile_form.is_valid():
            # Вежливо просим наши формы записать все, что написал в них юзер
            # в соответствующие таблицы в базе.
            user_form.save()
            # привязка профиля к пользователю
            user_instance = User.objects.get(username=user_form.cleaned_data['username'])
            profile_form = ProfileForm(request.POST, instance=user_instance.profile)
            profile_form.save()
            return HttpResponse('вы зарегистрированы') # временное решение
        # Тупой юзверь накосячил. Даем ему по ебалу.
        else:
            # Рендерим страницу регистрации, передаем туда заполненные формы, чтобы
            # пользователю не приходилось по 300 раз вводить одно и то же.
            return render(request, 'kubsu/reg.html', {
                'user_form': user_form,
                'profile_form': profile_form
                })
    # Если же использовался метод get, значит он еще не отправлял форму.
    # Инициализируем пустые формы и рендерим с ними страницу регистрации.
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
        return render(request, 'kubsu/reg.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            })
