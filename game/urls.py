from django.urls import path
from .views import search_game, game_detail, add_to_favorite, favorite_list

urlpatterns = [
    path('', search_game, name='search_game'),
    path('games/<int:pk>/', game_detail, name='game_detail'),
    path('games/<int:game_id>/add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('favorites/', favorite_list, name='favorite_list'),
]
