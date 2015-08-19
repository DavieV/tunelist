from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^signup/$', views.signup_view, name='signup_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^search/', include('haystack.urls')),
    url(r'^(?P<username>[0-9a-zA-Z_-]+)/$', views.profile, name='profile'),
    url(
        r'^(?P<username>[0-9a-zA-Z_-]+)/(?P<playlist_id>[0-9]+)/$',
        views.playlist,
        name='playlist'    
    ),
    url(
        r'^(?P<username>[0-9a-zA-Z_-]+)/(?P<playlist_id>[0-9]+)/delete/$',
        views.playlist_delete,
        name='playlist_delete'
    ),
    url(
        r'^(?P<username>[0-9a-zA-Z_-]+)/(?P<playlist_id>[0-9]+)/(?P<song_id>[0-9a-zA-Z_-]+)/$',
        views.song_delete,
        name='song_delete'
    ),
]
