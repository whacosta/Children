from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^inicio',login_required(views.HomeView.as_view()), name='home'),
    # url(r'^profile', views.ProfileView.as_view(), name='profile'),

    url(r'^perfil',login_required(views.ProfileView.as_view()), name='perfil'),
]
