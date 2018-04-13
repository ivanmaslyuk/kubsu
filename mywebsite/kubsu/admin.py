from django.contrib import admin

from .models import Profile, Document

# Register your models here.
admin.site.register(Profile)
admin.site.register(Document)

"Если не работает база: manage.py migrate --run-syncdb"