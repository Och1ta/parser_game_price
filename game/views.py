from django.shortcuts import render, redirect

from constans import URL_STEAM_SEARCH
from utils import parser_games_steam
from .models import Game


def get_game_name(request):
    if request.method == 'POST':
        data_input = request.POST.get('data_input')
        if not Game.objects.filter(name=data_input).exists():
            new_data = parser_games_steam(
                URL_STEAM_SEARCH.format(data_input),
                data_input
            )
            game_data = Game.objects.create(
                name=new_data[0],
                price=new_data[1],
                url=new_data[2]
            )
            game_data.save()
            return redirect('success_page')  # Перенаправляем на страницу успешного сохранения
        else:
            # Данные уже существуют в базе данных, обработка ошибки или вывод сообщения
            return render(
                request,
                'input_data.html',
                {'error_message': 'Data already exists!'}
            )

    return render(request, 'input_data.html')


def success_page_view(request):
    return render(request, 'success_page.html')
