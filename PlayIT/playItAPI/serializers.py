from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentityField
from rest_framework.fields import CharField
from appPlayIT.models import Pub, Playlist, Track, Review


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')
        groups=CharField(read_only=True)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class PubSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='playItAPI:pub-detail')
    user = HyperlinkedRelatedField(view_name='playItAPI:user-detail', read_only=True)
    playlists = HyperlinkedRelatedField(many=True, read_only=True, view_name='playItAPI:playlist-detail')
    class Meta:
        model = Pub
        fields = ('id', 'url', 'name', 'street', 'number', 'city', 'zipCode', 'stateOrProvince', 'country', 'user', 'playlists')


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='playItAPI:playlist-detail')
    user = HyperlinkedRelatedField(view_name='playItAPI:user-detail', read_only=True)
    pub = HyperlinkedRelatedField(view_name='playItAPI:pub-detail', read_only=True)
    class Meta:
        model = Playlist
        fields = ('id', 'url', 'pub', 'name', 'user')


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='playItAPI:track-detail')
    class Meta:
        model = Track
        fields = ('spotify_id', 'url', 'name', 'artist', 'album')


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='playItAPI:review-detail')
    pub = HyperlinkedRelatedField(view_name='playItAPI:pub-detail', read_only=True)
    user = CharField(read_only=True)

    class Meta:
        model = Review
        fields = ('url', 'rating', 'comment', 'user', 'date', 'pub')