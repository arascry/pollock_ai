from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add_text', views.add_text, name='add_text'),
    path('paintings/', views.PaintingsList.as_view(), name='index'),
    path('paintings/<int:pk>', views.PaintingsDetail.as_view(), name='detail'),
    path('paintings/create', views.PaintingsCreate.as_view(), name='paintings_create'),
    path('paintings/<int:pk>/update', views.PaintingsUpdate.as_view(), name='paintings_update'),
    path('paintings/<int:pk>/delete', views.PaintingsDelete.as_view(), name='paintings_delete'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/<int:pk>', views.user_detail, name='user_detail'),
]

