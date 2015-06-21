from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import PickyAuthenticationForm

def index(request):
    return render(request, 'home.html')

def log_in(request):
    form = PickyAuthenticationForm()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home-url')
        else:
            error = 'User account has been disabled'
            return render(request, 'login.html', {'form': form, 'error': error})
    else:
        error = 'Incorrect username or password!'
        return render(request, 'login.html', {'form': form, 'error': error})

def log_out(request):
    logout(request)
    return redirect('home-url')
