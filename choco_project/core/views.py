from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request, 'core/home.html')

def exit(request):
    logout(request)
    return redirect('home')
