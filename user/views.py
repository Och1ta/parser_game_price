from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def registration(request):
    """Страница регистрации пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('search_game')
    else:
        form = CustomUserCreationForm()
    return render(
        request, 'users/registration.html', {'form': form}
    )


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('search_game')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
