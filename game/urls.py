from django.urls import path
from .views import search_game, game_detail, add_to_favorite


urlpatterns = [
    path('', search_game, name='search_game'),
    path('games/<int:pk>/', game_detail, name='game_detail'),
    path('games/<int:pk>/add_to_favorite/', add_to_favorite, name='add_to_favorite'),
]
