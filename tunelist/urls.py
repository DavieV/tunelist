from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^', include('playlists.urls')),
    url(r'^admin/', include(admin.site.urls)),
]