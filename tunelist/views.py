from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm

def home(request):
    return render(request, 'home/index.html')

def signup_view(request):
    '''
    If the view is called with a POST request, then we register
    a new User. Otherwise we load a blank form for the user to
    enter their info.
    '''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # creates a new user and stores it in the database
            user = User.objects.create_user(
                request.POST['username'],
                request.POST['email'],
                request.POST['password1']
            )
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Invalid form info')
    else:
        form = RegistrationForm()
        return render(request, 'signup/signup.html', {'form' : form})

def login_view(request):
    '''
    If the view is called with a POST request, then we authenticate
    the user and log them in. Otherwise we load a blank login form.
    '''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Successfully logged in")
                else:
                    return HttpResponse("Inactive account")
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Invalid form info")
    else:
        form = LoginForm()
        return render(request, 'login/login.html', {'form' : form})
