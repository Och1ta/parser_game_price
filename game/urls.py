from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_game_name, name='get_game_name'),
    path('success/', views.success_page_view, name='success_page'),
]
