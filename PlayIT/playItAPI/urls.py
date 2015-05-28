from django.conf.urls import patterns, url,	include
from rest_framework.urlpatterns import format_suffix_patterns
from playItAPI.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'pubs', PubViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'tracks', TrackViewSet)

urlpatterns	= patterns('playItAPI.views',

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)