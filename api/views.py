from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, viewsets

from api.serializers import FavoriteGameSerializer, GameSerializer
from api.parsers import parser_games_steam
from game.constants import URL_STEAM_SEARCH
from game.models import Game, FavoriteGame
from user.models import User


class CustomUserViewSet(UserViewSet):
    """ViewSet модели User"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GameViewSet(viewsets.ModelViewSet):
    """View set for handling Game related operations."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(
        detail=False,
        methods=['post'],
        url_path='create',
        permission_classes=[IsAdminUser]
    )
    def create_game(self, request, *args, **kwargs):
        game_name = request.data.get('game_name')
        if not game_name:
            return Response(
                {'error': 'Please provide a game name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            game_title, game_price, game_url = parser_games_steam(URL_STEAM_SEARCH.format(game_name), game_name)
            existing_game = Game.objects.filter(name__iexact=game_title.lower()).first()
            if existing_game:
                serializer = self.get_serializer(existing_game)
                return Response(serializer.data)
            else:
                game = Game(name=game_title, old_price=None, new_price=game_price, url=game_url)
                game.save()
                serializer = self.get_serializer(game)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                {'error': 'Failed to parse game data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(
        detail=False,
        methods=['patch'],
        url_path='change_price',
        permission_classes=[IsAdminUser]
    )
    def change_price_game(self, request, *args, **kwargs):
        game_name = request.data.get('game_name')

        if not game_name:
            return Response(
                {'error': 'Please provide a game name'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(name__iexact=game_name.lower())

            _, new_game_price, _ = parser_games_steam(URL_STEAM_SEARCH.format(game_name), game_name)

            if new_game_price != game.new_price:
                game.old_price = game.new_price
                game.new_price = new_game_price
                game.save()

                serializer = self.get_serializer(game)
                return Response(serializer.data)
            else:
                return Response(
                    {'message': 'Price unchanged'},
                    status=status.HTTP_200_OK
                )
        except Game.DoesNotExist:
            return Response(
                {'error': 'Game not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response({
                'error': 'Failed to parse game data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FavoriteGameViewSet(viewsets.ModelViewSet):
    queryset = FavoriteGame.objects.all()
    serializer_class = FavoriteGameSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=['post'],
        url_path='add_to_favorite'
    )
    def add_to_favorite(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['delete'],
        url_path='delete_favorite/(?P<game_id>[0-9]+)'
    )
    def delete_favorite(self, request, game_id):
        favorite_game = get_object_or_404(FavoriteGame, user=request.user, game_id=game_id)
        if favorite_game:
            favorite_game.delete()
            return Response(
                {'message': 'Game removed from favorites'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'error': 'Game not found in favorites'},
            status=status.HTTP_404_NOT_FOUND
        )
