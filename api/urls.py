from django.contrib.auth.views import LogoutView
from django.urls import path

from api.views import SearchGame, GameDetailView, UserViewSet, FavoriteGameViewSet

urlpatterns = [
    path('', SearchGame.as_view(), name='search_game'),
    path(
        'game/<int:pk>/',
        GameDetailView.as_view(),
        name='game_detail'
    ),
    path(
        'register/',
        UserViewSet.as_view({'get': 'register_page', 'post': 'create'}),
        name='user_registration'
    ),
    path(
        'profile/',
        UserViewSet.as_view({'get': 'profile_page'}),
        name='user_profile_page'
    ),
    path(
        'login/',
        UserViewSet.as_view({'get': 'login_page', 'post': 'login'}),
        name='user_login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'favorite/<int:pk>/add_to_favorite/',
        FavoriteGameViewSet.as_view({'post': 'add_to_favorite'}),
        name='add_to_favorite'
    ),
    path(
        'favorite/<int:pk>/delete_favorite/',
        FavoriteGameViewSet.as_view({'post': 'delete_favorite'}),
        name='delete_favorite'
    ),
]
