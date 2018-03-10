from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # Следующие поля нам не нужны, т.к. они уже есть в модели User (стандартная из Django),
    # к которой Profile "цепляется".

    #username = models.CharField(max_length=50)
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=50)
    #password = models.CharField(max_length=20)
    #email = models.EmailField()

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

    path = models.CharField(max_length=250, verbose_name='Направление') # направление
    course = models.IntegerField(default=1, verbose_name='Курс') # курс
    
    def __str__(self):
        if self.user.is_staff:
            return 'Администратор {}'.format(self.user.username)
        else:
            return '{0} ({1}, {2}, {3} курс)'.format(
                    self.user.get_full_name(), 
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

