from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from api.serializers import UserSerializer, FavoriteGameSerializer
from game.constants import URL_STEAM_SEARCH
from game.models import Game, FavoriteGame
from game.utils import parser_games_steam
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get']
    )
    def register_page(self, request):
        return render(request, 'users/registration_page.html')

    @action(
        detail=False,
        methods=['get']
    )
    def login_page(self, request):
        return render(request, 'users/login_page.html')

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def profile_page(self, request):
        user = request.user
        favorite_games = FavoriteGame.objects.filter(user=user)
        favorite_game_names = {
            game.game.id: game.game.name for game in favorite_games
        }
        return render(
            request,
            'users/profile_page.html',
            {'user': user, 'favorite_game_names': favorite_game_names}
        )

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['post']
    )
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Successfully logged in.'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class SearchGame(APIView):
    """..."""

    def get(self, request):
        """..."""
        return render(request, 'games/search_game.html')

    def post(self, request):
        """..."""
        name = request.data.get('data_input')
        if not name:
            return Response(
                {'error': 'Please provide a game name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        existing_game = Game.objects.filter(name__iexact=name.lower()).first()
        if existing_game:
            return redirect('game_detail', pk=existing_game.pk)
        else:
            try:
                game_title, game_price, game_url = parser_games_steam(
                    URL_STEAM_SEARCH.format(name),
                    name
                )
                game = Game(name=game_title, price=game_price, url=game_url)
                game.save()
                return redirect('game_detail', pk=game.pk)
            except Exception:
                return Response(
                    {'error': 'Failed to parse game data'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class GameDetailView(DetailView):
    """..."""

    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'


class FavoriteGameViewSet(viewsets.ViewSet):
    queryset = FavoriteGame.objects.all()
    serializer_class = FavoriteGameSerializer

    @action(
        detail=True,
        methods=['post']
    )
    def add_to_favorite(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        favorite_game, created = FavoriteGame.objects.get_or_create(
            user=request.user,
            game=game
        )
        if created:
            return Response(
                {'detail': 'Game added to favorites.'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'detail': 'Game already in favorites.'},
                status=status.HTTP_200_OK
            )

    @action(detail=True, methods=['post'])
    def delete_favorite(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        favorite_game = get_object_or_404(FavoriteGame, user=request.user, game=game)
        favorite_game.delete()
        return Response(
            {'detail': 'Game removed from favorites.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def favorite_games(self, request):
        favorite_game = FavoriteGame.objects.filter(user=request.user)
        serializer = self.serializer_class(favorite_game, many=True)
        return Response(serializer.data)
