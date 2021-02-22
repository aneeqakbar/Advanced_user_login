from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Profile
from .tokens import account_activation_token
from django.template.loader import render_to_string

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'user/index.html',{'loggedin':True})
    return render(request, 'user/index.html',{'loggedin':False})

def activation_sent_view(request):
    return render(request, 'user/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('User:home'))
        # return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        # form.save()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=password)
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.bio = form.cleaned_data.get('bio')
        # user can't login until link confirmed
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        print(current_site)
        subject = 'Please Activate Your Account'
        # load a template like get_template() 
        # and calls its render() method immediately.
        message = render_to_string('user/activation_request.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # method will generate a hash value with user related data
            'token': account_activation_token.make_token(user),
        })
        # print(message)
        user.email_user(subject, message)
        return HttpResponseRedirect(reverse('User:activation_sent'))
        # return redirect('activation_sent')
        # user.save() # post_save function at models.py triggers here
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password1')
        # login(request, user)
        # user = authenticate(username=username, password=password)
    else:
        # form = SignUpForm()
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
        