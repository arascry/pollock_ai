from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_text', views.add_text, name='add_text')
]