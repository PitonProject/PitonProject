from django.shortcuts import render, render_to_response
from SpotifyAPI.spotify import SpotifyBrowser
from django.contrib.auth.models import User
from appPlayIT.models import *

# Create your views here.
def mainpage(request):
    pubs = None
    if request.user:
        pubs = Pub.objects.filter(id__in=User.objects.get(username=request.user).user_pub_set.all())
    return render_to_response(
        'mainpage.html',
        {
                'titlehead': 'PlayIT app',
                'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local',
                'user': request.user,
                'pubs' : pubs
        })

def browse_track(request, keyword, offset, limit, next_page):
    return render_to_response(
        'browse_track.html',
        {
            'titlehead' : 'PlayIT - Browse Track',
            'pagetitle' : 'Search a Track on Spotify',
            'user' : request.user,
            'keyword' : keyword,
            'tracks' : SpotifyBrowser.search_track(keyword, offset, limit)["tracks"],
            'next_page' : next_page
        }
    )

def browse_artist(request, keyword, offset, limit, next_page):
    return render_to_response(
        'browse_artist.html',
        {
            'titlehead' : 'PlayIT - Browse Artist',
            'pagetitle' : 'Search an Artist on Spotify',
            'user' : request.user,
            'keyword' : keyword,
            'artists' : SpotifyBrowser.search_artist(keyword, offset, limit)["artists"],
            'next_page' : next_page
        }
    )

def browse_album(request, keyword, offset, limit, next_page):
    return render_to_response(
        'browse_album.html',
        {
            'titlehead' : 'PlayIT - Browse Album',
            'pagetitle' : 'Search an Album on Spotify',
            'user' : request.user,
            'keyword' : keyword,
            'albums' : SpotifyBrowser.search_album(keyword, offset, limit)["albums"],
            'next_page' : next_page
        }
    )

def browse_playlist(request, keyword, offset, limit, next_page):
    return render_to_response(
        'browse_playlist.html',
        {
            'titlehead' : 'PlayIT - Browse Playlist',
            'pagetitle' : 'Search a Playlist on Spotify',
            'user' : request.user,
            'keyword' : keyword,
            'playlists' : SpotifyBrowser.search_playlist(keyword, offset, limit)["playlists"],
            'next_page' : next_page
        }
    )

def browse(request):
    type = request.GET.get('type')
    keyword = request.GET.get('keyword')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 50))
    if not type or not keyword:
        return render_to_response(
            'browse.html',
            {
                    'titlehead': 'PlayIT - Browse',
                    'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local',
                    'user': request.user
            })
    else:
        next_page = "/browse?keyword=" + keyword + "&type=" + type + "&limit=" + str(limit) + "&offset=" + str(offset+limit)
        if type == 'track':
            return browse_track(request, keyword, offset, limit, next_page)
        elif type == 'artist':
            return browse_artist(request, keyword, offset, limit, next_page)
        elif type == 'album':
            return browse_album(request, keyword, offset, limit, next_page)
        elif type == 'playlist':
            return browse_playlist(request, keyword, offset, limit, next_page)

def track(request, track_id):
    return render_to_response(
        'track.html',
        {
            'titlehead' : 'PlayIT - Add Track to Pub Playlist',
            'pagetitle' : 'Add a Spotify Track to a Pub Playlist',
            'user' : request.user,
            'track' : SpotifyBrowser.get_track_by_id(track_id)
        }
    )

def get_pub_list(request):
    return render_to_response(
        'pub_list.html',
        {
            'titlehead' : 'PlayIT - View Pub List',
            'pagetitle' : 'View All Pubs',
            'pubs' : Pub.objects.all()
        }
    )

def get_pub(request, pub_id):
    return render_to_response(
        'pub.html',
        {
            'titlehead' : 'PlayIT - View a Pub',
            'pagetitle' : 'View Pub detail',
            'pub' : Pub.objects.get(id=pub_id),
            'playlists' : Playlist.objects.filter(id_pub=pub_id)
        }
    )

def get_playlist_list(request):
    return render_to_response(
        'playlist_list.html',
        {
            'titlehead' : 'PlayIT - View Playlist List',
            'pagetitle' : 'View All Playlists',
            'playlists' : Playlist.objects.all()
        }
    )
def get_playlist(request, playlist_id):
    return render_to_response(
        'playlist.html',
        {
            'titlehead' : 'PlayIT - View a Playlist',
            'pagetitle' : 'View Playlist Tracks',
            'playlist' : Playlist.objects.get(id=playlist_id),
            'tracks' : Track.objects.filter(playlist_track__in=Playlist_Track.objects.filter(id_playlist=playlist_id))
        }
    )