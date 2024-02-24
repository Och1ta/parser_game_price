from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
]
