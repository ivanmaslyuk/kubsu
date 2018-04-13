import os
import time

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # Устанавливаем отношение один-к-одному между моделями Profile и User,
    # то есть каждому User соответствует Profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    FACULTY_CHOICES = (
        ('ФТФ', 'Физико-технический факультет'),
        ('ФПМ', 'Факультет прикладной математики'),
    )

    faculty = models.CharField(
        max_length=10,
        verbose_name='Факультет',
        choices=FACULTY_CHOICES,
        )

    def get_full_name(self):
        return '{0} {1} {2}'.format(
            self.last_name if self.last_name != '' else 'ФАМИЛИЯ',
            self.first_name if self.first_name != '' else 'ИМЯ',
            self.father_name if self.father_name != '' else 'ОТЧЕСТВО'
        )
    
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    father_name = models.CharField(max_length=50, verbose_name='Отчество')
    path = models.CharField(max_length=250, verbose_name='Направление') # направление
    course = models.IntegerField(default=1, verbose_name='Курс') # курс
    
    def __str__(self):
        if self.user.is_staff:
            return 'Администратор {}'.format(self.user.username)
        else:
            return '{0} ({1}, {2}, {3} курс)'.format(
                    self.get_full_name(), 
                    self.faculty if self.faculty != '' else 'не задан факультет',
                    self.path if self.path != '' else 'не задано направление',
                    self.course
                )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    

class Document(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Выберите файл', upload_to='documents')
    title = models.CharField(max_length=300)

    def __str__(self):
        prof = self.owner
        return '{0} ({1}, {2}, {3}, {4} курс)'.format(
            self.title,
            prof.get_full_name(),
            prof.faculty,
            prof.path,
            prof.course,
        )