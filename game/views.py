from django.shortcuts import render, redirect

from .models import GameName


def get_game_name(request):
    if request.method == 'POST':
        data_input = request.POST.get('data_input')
        if not GameName.objects.filter(name=data_input).exists():
            new_data = GameName(name=data_input)
            new_data.save()
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
