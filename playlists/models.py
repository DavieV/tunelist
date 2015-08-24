import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# For User creation signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# TODO: add e-mail verification flag to this model
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    @property
    def num_playlists(self):
        return self.user.playlist_set.all().count()

    def __str__(self):
        return self.user.get_username()

# Create your models here.
class Playlist(models.Model):
    author = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    num_likes = models.PositiveIntegerField(default=0)

    def count(self):
        return self.song_set.all().count()

    def __str__(self):
        return self.name

class Song(models.Model):
    playlist = models.ForeignKey(Playlist)
    song_url = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    '''
    Whenever a new user is created, we also create their user profile
    '''
    if created:
        profile = UserProfile.objects.create(user = instance)
