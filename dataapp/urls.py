from django.contrib import admin
from django.urls import path
from dataapp import views
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
]

