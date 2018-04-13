from django.urls import path

from . import views

app_name = 'kubsu'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('', views.profile.as_view(), name='profile'),
    path('logout-user/', views.logout_user, name='logout-user'),
    path('compose/', views.compose, name='compose'),
    path('delete-doc/', views.delete_doc, name='delete-doc')
]
