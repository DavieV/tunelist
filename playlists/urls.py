from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^signup/$', views.signup_view, name='signup_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(
        r'^(?P<username>.*)/(?P<playlist_id>.*)/delete/$',
        views.playlist_delete,
        name='playlist_delete'
    ),
    url(
        r'^(?P<username>.*)/(?P<playlist_id>.*)/(?P<song_id>.*)/$',
        views.song_delete,
        name='song_delete'
    ),
    url(
        r'^(?P<username>.*)/(?P<playlist_id>.*)/$',
        views.playlist,
        name='playlist'
    ),
    url(r'^(?P<username>.*)/$', views.profile, name='profile'),
    url(r'^explore/?$', views.explore),
]
