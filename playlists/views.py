import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from .models import Playlist, Song
from .forms import PlaylistForm, SongForm, LoginForm, RegistrationForm

def index(request):
    return render(request, 'playlists/index.html', {})

def profile(request, username):
    '''
    The profile page that displays the playlists of a given user.
    If the user is logged in, then a form to add new playlists is also
    displayed.
    '''
    user = get_object_or_404(User, username=username)
    playlists = Playlist.objects.filter(author=user).order_by('pk')
    context = {'playlists' : playlists, 'username' : username}

    if request.user == user:
        if request.method == 'POST':
            form = PlaylistForm(request.POST)
            if form.is_valid():
                playlist = Playlist.objects.create(
                    author = user,
                    name = request.POST['name'],
                )
                return HttpResponseRedirect('') # reload the page
            return HttpResponse("invalid form info")
        form = PlaylistForm()
        context['form'] = form
    return render(request, 'playlists/profile.html', context)

def playlist(request, username, playlist_id):
    '''
    View for listening to an existing playlist. If the user is viewing
    their own playlist then the option to add a song to the playlist
    is present.

    If the view is called via a POST request then the form is processed and
    a new song is added to the playlist
    '''
    user = get_object_or_404(User, username=username)
    playlist = get_object_or_404(Playlist, author=user, pk=playlist_id)
    context = {'username' : username, 'playlist' : playlist}

    if request.user == user:
        if request.method == 'POST':
            form = SongForm(request.POST)
            if form.is_valid():
                song_url = request.POST['song_url']
                song_id = song_url.split('=')[1]

                # Verify that the song_id is unique to this playlist
                for s in playlist.song_set.all():
                    if s.song_url.split('=')[1] == song_id:
                        return HttpResponse("This song is already in the playlist")

                song = Song.objects.create(
                    playlist = playlist,
                    song_url = song_url,
                    name = request.POST['name'],
                    artist = request.POST['artist'],
                )
                playlist.save()
                return HttpResponseRedirect('') # reload this page
            return HttpResponse("invalid form info")
        form = SongForm()
        context['form'] = form
    return render(request, 'playlists/playlist.html', context)

@login_required
def playlist_delete(request, username, playlist_id):
    '''
    View to to delete a user's specified playlist
    '''
    user = get_object_or_404(User, username=username)

    # Check if currently signed in user is viewing their own profile
    if request.user != user:
        return HttpResponseRedirect('/')  # send the user back to the homepage

    playlist = get_object_or_404(Playlist, author=user, pk=playlist_id)
    playlist.delete()
    user.profile.save()
    return HttpResponse("Playist deleted.")

@login_required
def song_delete(request, username, playlist_id, song_id):
    user = get_object_or_404(User, username=username)

    # Check if the logged in user is viewing their own profile
    if request.user != user:
        return HttpResponseRedirect('/playlists/')

    song = get_object_or_404(Song, pk=song_id, playlist=playlist)
    song.delete()

    return HttpResponse("Song removed.")

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
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponse("Inactive account")
            else:
                return HttpResponse("Invalid username or password")
        else:
            return HttpResponse("Invalid form info")
    else:
        form = LoginForm()
        return render(request, 'login/login.html', {'form' : form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
