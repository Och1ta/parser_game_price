import logging
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from api.serializers import FavoriteGameSerializer, GameSerializer
from api.parsers import parser_games_steam
from game.constants import URL_STEAM_SEARCH
from game.models import Game, FavoriteGame
from user.models import User


logger = logging.getLogger(__name__)


class CustomUserViewSet(UserViewSet):
    """View set for handling User related operations."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GameViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """View set for handling Game related operations."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(
        detail=False,
        methods=['post'],
        url_path='parse_game',
        permission_classes=[IsAdminUser]
    )
    def parse_game(self, request):
        """Parse game data from Steam API and add it to the database."""
        game_name = request.data.get('game_name')
        if not game_name:
            return Response(
                {'error': 'Please provide a game name'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game_title, game_price, game_url = parser_games_steam(
                URL_STEAM_SEARCH.format(game_name),
                game_name
            )
            existing_game = Game.objects.filter(
                name__iexact=game_title.lower()
            ).first()

            if existing_game:
                serializer = self.get_serializer(existing_game)
                return Response(serializer.data)

            else:
                game = Game(
                    name=game_title, old_price=None,
                    new_price=game_price, url=game_url
                )
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
        url_path='update',
        permission_classes=[IsAdminUser]
    )
    def update_price(self, request):
        """Update game price manually."""
        game_name = request.data.get('game_name')
        new_price = request.data.get('new_price')

        if not game_name or new_price is None:
            return Response(
                {'error': 'Please provide both game name and new price'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(name__iexact=game_name.lower())
            game.new_price = new_price
            game.save()
            return Response({'message': 'Price updated successfully'}, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(
                {'error': 'Game not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FavoriteGameViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """View set for handling FavoriteGame related operations."""

    queryset = FavoriteGame.objects.all()
    serializer_class = FavoriteGameSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=['post'],
        url_path='add'
    )
    def add_to_favorite(self, request):
        """Add a game to user's favorite list."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['delete'],
        url_path='delete/(?P<game_id>[0-9]+)'
    )
    def delete_favorite(self, request, game_id):
        """Remove a game from user's favorite list."""
        favorite_game = get_object_or_404(
            FavoriteGame, user=request.user, game_id=game_id
        )

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

    @action(
        detail=False,
        methods=['patch'],
        url_path='check_price'
    )
    def check_price(self, request):
        """Check and update price for a favorite game."""
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
                logger.info(
                    f'Цена изменена для игры {game.name}: '
                    f'{game.new_price} -> {new_game_price}'
                )
                game.old_price = game.new_price
                game.new_price = new_game_price
                game.save()
                serializer = GameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({'message': 'Price unchanged'}, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response(
                {'error': 'Game not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
