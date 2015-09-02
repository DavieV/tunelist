from django.contrib import admin

from .models import Song, Playlist, UserProfile

class SongInline(admin.TabularInline):
    model = Song
    extra = 1

class PlaylistAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['name', 'author', 'genre', 'num_likes']}),
        ('Date Information', {'fields' : ['pub_date'], 'classes' : ['collapse']}),
    ]
    inlines = [SongInline]

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields' : ['user']})]

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
