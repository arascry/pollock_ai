from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add_text', views.add_text, name='add_text'),
    path('paintings/', views.PaintingsList.as_view(), name='index'),
    path('paintings/<int:pk>', views.PaintingsDetail.as_view(), name='detail'),

    path('accounts/signup', views.signup, name='signup'),
]

