import os
import time

from docxtpl import DocxTemplate

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings

from .models import Document
from .forms import ProfileForm, UserRegistrationForm, DocumentForm


def auth(request):
    if request.user.is_authenticated:
        return redirect('kubsu:profile')
    # Если для открытия страницы использовался метод post,
    # значит нужно обработать данные для регистрации.
    if request.method == 'POST':
        # Создаем экземпляры форм и заполняем их полученной информацией.
        user_form = UserRegistrationForm(request.POST)
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
            login(request, user_instance) # здесь же и логиним пользователя
            
            return HttpResponse('вы зарегистрированы') # временное решение
        # Пользователь ввел неправильные данные.
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
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'kubsu/reg.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            })

class profile(LoginRequiredMixin, View):
    
    # Страница, на которую будет перенаправлен пользователь, если он не вошел в систему.
    login_url = 'kubsu:auth'

    # Обрататывает get-запросы к странице.
    def get(self, request, *args, **kwargs):
        edit_profile_form = ProfileForm(instance=request.user.profile)
        upload_document_form = DocumentForm()

        documents = Document.objects.filter(owner=request.user.profile)

        return render(request, 'kubsu/profile.html', {
            'edit_profile_form': edit_profile_form,
            'upload_document_form': upload_document_form,
            'documents': documents,
        })

    # Обрабатывает post-запросы к странице.
    def post(self, request, *args, **kwargs):
        edit_profile_form = ProfileForm(request.POST)
        upload_document_form = DocumentForm(request.POST, request.FILES)

        # Обработка формы для обновления профиля.
        if edit_profile_form.is_valid():
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            profile_form.save()
            return self.get(request)

        # Обработка формы для загрузки документов.
        elif upload_document_form.is_valid():
            upload_document_form.instance.owner = request.user.profile
            upload_document_form.save()
            return self.get(request)

        if settings.DEBUG:
            return HttpResponse('ни одна форма не прошла тест на валидность')
        else:
            return self.get(request)

def logout_user(request):
    logout(request)
    return redirect('kubsu:auth')

@login_required(login_url='kubsu:auth')
def compose(request):
    template_path = os.path.join(settings.BASE_DIR, 'kubsu/templates/kubsu/zayav_template.docx')
    file_name = request.user.username + '_' + str(int(time.time())) + '.docx'
    file_path = os.path.join(settings.MEDIA_ROOT, 'pleas/' + file_name)
    doc = DocxTemplate(template_path)
    context = {
        'profile': request.user.profile,
    }
    doc.render(context)
    doc.save(file_path)
    return HttpResponse('Сгенерированный документ')

@login_required(login_url='kubsu:auth')
def delete_doc(request):
    try:
        doc_id = int(request.GET['doc_id'])
        doc = Document.objects.get(pk=doc_id, owner=request.user.profile)
        doc.delete()
    finally:
        return redirect('kubsu:profile')