from django.urls import path
from . import views

#add all the paths that you want ( path, render from views.py, name of URL)

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
]