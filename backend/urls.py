from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration', include('user.urls'), name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('game.urls'), name='games'),
]
