from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GameViewSet, CustomUserViewSet, FavoriteGameViewSet

app_name = 'api'

router = DefaultRouter()

router.register('games', GameViewSet, basename='games')
router.register('users', CustomUserViewSet, basename='users')
router.register('favorite', FavoriteGameViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
