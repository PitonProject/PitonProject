from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from appPlayIT.views import *
from appPlayIT.forms import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PlayIT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include('playItAPI.urls', namespace='playItAPI')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^$', mainpage, name='home'),
    url(r'^browse$', browse),
    url(r'^track/$', track_list),
    url(r'^track.json/$', track_list_json),
    url(r'^track.xml/$', track_list_xml),
    url(r'^track/(\w+)/$', track),
    url(r'^pub/$', get_pub_list),
    url(r'^pub.json/$', get_pub_list_json),
    url(r'^pub.xml/$', get_pub_list_xml),
    url(r'^pub/(\d+)/$', get_pub),
    url(r'^pub/(?P<pk>\d+)/edit/$', LoginRequiredCheckIsOwnerUpdateView.as_view(model=Pub, form_class=PubForm), name='pub_edit'),
    url(r'^pub/(?P<pk>\d+)/delete/$', LoginRequiredCheckIsOwnerDeleteView.as_view(model=Pub), name='pub_delete'),
    url(r'^pub/create/$', PubCreate.as_view(), name='pub_create'),
    url(r'^pub/(?P<pk>\d+)/playlist/create/$', PlaylistCreate.as_view(), name='playlist_create'),
    url(r'^pub/(?P<pkr>\d+)/playlist/(?P<pk>\d+)/edit/$', LoginRequiredCheckIsOwnerUpdateView.as_view(model=Playlist, form_class=PlaylistForm), name='playlist_edit'),
    url(r'^pub/(?P<pkr>\d+)/playlist/(?P<pk>\d+)/delete/$', LoginRequiredCheckIsOwnerDeleteView.as_view(model=Playlist), name='playlist_delete'),
    url(r'^pub/(\d+).xml/$', get_pub_xml),
    url(r'^pub/(\d+).json/$', get_pub_json),
    url(r'^pub/(\d+)/playlist.json/$', get_pub_playlists_json),
    url(r'^pub/(\d+)/playlist.xml/$', get_pub_playlists_xml),
    url(r'^playlist/$', get_playlist_list),
    url(r'^playlist.json/$', get_playlist_list_json),
    url(r'^playlist.xml/$', get_playlist_list_xml),
    url(r'^playlist/(\w+)/$', get_playlist),
    url(r'^playlist/(\w+).json/$', get_playlist_json),
    url(r'^playlist/(\w+).xml/$', get_playlist_xml),
    url(r'^playlist/(\w+)/track.json/$', get_playlist_tracks_json),
    url(r'^playlist/(\w+)/track.xml/$', get_playlist_tracks_xml)
)
