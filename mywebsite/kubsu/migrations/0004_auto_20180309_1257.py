# Generated by Django 2.0.2 on 2018-03-09 12:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kubsu', '0003_auto_20180309_1236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentProfile',
            new_name='Student',
        ),
    ]
