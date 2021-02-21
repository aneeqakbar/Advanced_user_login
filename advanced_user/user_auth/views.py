from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.shortcuts import render, redirect
from .models import Profile

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'user/index.html',{'loggedin':True})
    return render(request, 'user/index.html',{'loggedin':False})

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        # form.save()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=password)
        user = form.save()
        user.refresh_from_db()
        print(user.profile)
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.bio = form.cleaned_data.get('bio')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        login(request, user)
        user = authenticate(username=username, password=password)
        return HttpResponseRedirect(reverse('User:home'))
    else:
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form': form})
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('User:signup'))

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('User:home'))

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('User:home'))
        else:
            form = AuthenticationForm()
            return render(request,'user/login.html',{'form' : form,"message":"Invalid Credentials"})
    form = AuthenticationForm()
    return render(request,'user/login.html',{'form' : form})
        