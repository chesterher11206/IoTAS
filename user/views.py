from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print(form.errors)
    return render(request, 'user/login.html', {'form': form})

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('log_in'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('log_in'))
        else:
            print(form.errors)
    return render(request, 'user/signup.html', {'form': form})


# Create your views here.
