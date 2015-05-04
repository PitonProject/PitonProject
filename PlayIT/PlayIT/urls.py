from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from appPlayIT.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PlayIT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^$', mainpage, name='home'),
    url(r'^browse$', browse),
    url(r'^track/$', track_list),
    url(r'^track.json/$', track_list_json),
    url(r'^track.xml/$', track_list_xml),
    url(r'^track/(\w+)/$', track),
    url(r'^pub/$', get_pub_list),
    url(r'^pub.json/$', get_pub_list_json),
    url(r'^pub.xml/$', get_pub_list_xml),
    url(r'^pub/(\w+)/$', get_pub),
    url(r'^pub/(\w+).xml/$', get_pub_xml),
    url(r'^pub/(\w+).json/$', get_pub_json),
    url(r'^playlist/$', get_playlist_list),
    url(r'^playlist.json/$', get_playlist_list_json),
    url(r'^playlist.xml/$', get_playlist_list_xml),
    url(r'^playlist/(\w+)/$', get_playlist),
    url(r'^playlist/(\w+).json/$', get_playlist_json),
    url(r'^playlist/(\w+).xml/$', get_playlist_xml),
    url(r'^playlist/(\w+)/track.json/$', get_playlist_tracks_json),
    url(r'^playlist/(\w+)/track.xml/$', get_playlist_tracks_xml)
)
