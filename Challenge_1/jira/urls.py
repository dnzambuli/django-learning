from django.urls import path
from . import views

# define url patters

urlpatterns = [
    path('', views.index, name='index'),
]