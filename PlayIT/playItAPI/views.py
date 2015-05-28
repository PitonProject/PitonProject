from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from appPlayIT.models import Pub, Playlist, Track, Review
from playItAPI.serializers import UserSerializer, GroupSerializer, PubSerializer, PlaylistSerializer, TrackSerializer, ReviewSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API
    """
    return Response({
        'users': reverse('user-list', vrequest=request),
        'groups': reverse('group-list', request=request),
        'pubs': reverse('pub-list', request=request),
        'reviews': reverse('reviews-list', request=request),
        'playlists': reverse('playlists-list', request=request),
        'tracks': reverse('track-list', request=request),
    })


class UserList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of users
    """
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single users
    """
    model = User
    serializer_class = UserSerializer


class PubList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of pubs
    """
    queryset = Pub.objects.all()
    model = Pub
    serializer_class = PubSerializer


class PubDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single pubs
    """
    model = Pub
    serializer_class = PubSerializer


class PlaylistList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of playlists
    """
    queryset = Playlist.objects.all()
    model = Playlist
    serializer_class = PlaylistSerializer


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single playlist
    """
    model = Playlist
    serializer_class = PlaylistSerializer


class TrackList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of tracks
    """
    queryset = Track.objects.all()
    model = Track
    serializer_class = TrackSerializer


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single track
    """
    model = Track
    serializer_class = TrackSerializer


class GroupList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of groups
    """
    model = Group
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single group
    """
    model = Group
    serializer_class = GroupSerializer


class ReviewList(generics.ListCreateAPIView):
    """
      API endpoint that	represents a list of reviews
    """
    model = Review
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
      API endpoint that	represents a single review
    """
    model = Review
    serializer_class = ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pubs to be viewed or edited.
    """
    queryset = Pub.objects.all()
    serializer_class = PubSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows playlists to be viewed or edited.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows track to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows review to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
