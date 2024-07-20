from celery import shared_task
from django.urls import reverse
from rest_framework.test import APIRequestFactory
import logging

from api.views import FavoriteGameViewSet


logger = logging.getLogger(__name__)


@shared_task
def check_price_game_task():
    factory = APIRequestFactory()
    view = FavoriteGameViewSet.as_view({'patch': 'check_price'})

    game_name = 'game_name'

    request = factory.patch(reverse('game-check_price_game'), {'game_name': game_name})

    response = view(request)

    if response.status_code == 200:
        return 'Price checked successfully'
    else:
        return f'Failed to check price: {response.data}'
