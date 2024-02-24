from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect

from constans import URL_STEAM_SEARCH
from utils import parser_games_steam
from .models import Game, FavoriteGame


def search_game(request):
    if request.method == 'POST':
        data_input = request.POST.get('data_input')
        if data_input:
            if not Game.objects.filter(name=data_input).exists():
                game_data = parser_games_steam(
                    URL_STEAM_SEARCH.format(data_input),
                    data_input
                )
                game = Game.objects.create(
                    name=game_data[0],
                    price=game_data[1],
                    url=game_data[2]
                )
                game.save()
            else:
                game = Game.objects.get(name=data_input)
            return redirect('game_detail', pk=game.pk)
        else:
            return HttpResponseBadRequest("Название игры не было предоставлено")
    else:
        return render(request, 'games/search_game.html')


def game_detail(request, pk):
    game = Game.objects.get(pk=pk)
    return render(request, 'games/game_detail.html', {'games': game})


@login_required
def add_to_favorite(request, game_id):
    game = Game.objects.get(pk=game_id)
    favorite = FavoriteGame(user=request.user, game=game)
    favorite.save()
    return redirect('game_detail', pk=game_id)


@login_required
def favorite_list(request):
    favorites = FavoriteGame.objects.filter(user=request.user)
    return render(request, 'games/favorite_games.html', {'favorites': favorites})
