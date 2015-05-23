from django.shortcuts import render, render_to_response
from SpotifyAPI.spotify import SpotifyBrowser
from django.contrib.auth.models import User
from appPlayIT.models import *
from django.http import Http404, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from appPlayIT.forms import *
from django.core.exceptions import PermissionDenied

# Create your views here.
def mainpage(request):
    pubs = None
    if request.user.is_authenticated():
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
                    'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local'
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

def render_json_response(objects):
    json_data = serializers.serialize(u"json", objects)
    return HttpResponse(json_data, content_type=u"application/json")

def render_xml_response(objects):
    json_data = serializers.serialize(u"xml", objects)
    return HttpResponse(json_data, content_type=u"application/xml")

def track_list_json(request):
    return track_list(request, 'json')

def track_list_xml(request):
    return track_list(request, 'xml')

def track_list(request, format='html'):
    tracks = Track.objects.all()
    if format == 'xml':
        return render_xml_response(tracks)
    elif format == 'json':
        return render_json_response(tracks)
    else:
        return render_to_response(
            'track_list.html',
            {
                'titlehead' : 'PlayIT - View all registered Tracks',
                'pagetitle' : 'View All Tracks',
                'tracks' : tracks
            }
        )

def track(request, track_id):
    pubs = None
    if request.user.is_authenticated:
        pubs = Pub.objects.filter(id__in=User.objects.get(username=request.user).user_pub_set.all())
    return render_to_response(
        'track.html',
        {
            'titlehead' : 'PlayIT - Add Track to Pub Playlist',
            'pagetitle' : 'Add a Spotify Track to a Pub Playlist',
            'user' : request.user,
            'pubs' : pubs,
            'track' : SpotifyBrowser.get_track_by_id(track_id)
        }
    )

def get_pub_list_json(request):
    return get_pub_list(request, 'json')

def get_pub_list_xml(request):
    return get_pub_list(request, 'xml')

def get_pub_list(request, format='html'):
    pubs = Pub.objects.all()
    if format == 'json':
        return render_json_response(pubs)
    elif format == 'xml':
        return render_xml_response(pubs)
    else:
        return render_to_response(
            'pub_list.html',
            {
                'titlehead' : 'PlayIT - View Pub List',
                'pagetitle' : 'View All Pubs',
                'pubs' : pubs
            }
        )

def get_pub_json(request, pub_id):
    return get_pub(request, pub_id, 'json')

def get_pub_xml(request, pub_id):
    return get_pub(request, pub_id, 'xml')

def get_pub(request, pub_id, format='html'):
    try:
        pub = Pub.objects.get(id=pub_id)
    except:
        raise Http404('Pub not found.')
    if format == 'json':
        return render_json_response([pub,])
    elif format == 'xml':
        return render_xml_response([pub,])
    else:
        return render_to_response(
            'pub.html',
            {
                'titlehead' : 'PlayIT - ' + pub.name,
                'pagetitle' : 'View Pub: ' + pub.name,
                'pub' : pub,
                'playlists' : Playlist.objects.filter(id_pub=pub_id)
            }
        )

def get_pub_playlists_json(request, pub_id):
    return get_pub_playlists(request, pub_id, 'json')

def get_pub_playlists_xml(request, pub_id):
    return get_pub_playlists(request, pub_id, 'xml')

def get_pub_playlists(requests, pub_id, format='html'):
    try:
        pub = Pub.objects.get(id=pub_id)
        playlists = Playlist.objects.filter(id_pub=pub_id)
    except:
        raise Http404('Pub not found.')
    if format == 'json':
        return render_json_response(playlists)
    elif format == 'xml':
        return render_xml_response(playlists)

def get_playlist_list_json(request):
    return get_playlist_list(request, 'json')

def get_playlist_list_xml(request):
    return get_playlist_list(request, 'xml')

def get_playlist_list(request, format='html'):
    playlists = Playlist.objects.all()
    if format == 'json':
        return render_json_response(playlists)
    elif format == 'xml':
        return render_xml_response(playlists)
    else:
        return render_to_response(
            'playlist_list.html',
            {
                'titlehead' : 'PlayIT - View Playlist List',
                'pagetitle' : 'View All Playlists',
                'playlists' : playlists
            }
        )

def get_playlist_json(request, playlist_id):
    return get_playlist(request, playlist_id, 'json')

def get_playlist_xml(request, playlist_id):
    return get_playlist(request, playlist_id, 'xml')

def get_playlist(request, playlist_id, format='html'):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        raise Http404('Playlist not found.')
    if format == 'json':
        return render_json_response([playlist,])
    elif format == 'xml':
        return render_xml_response([playlist,])
    else:
        return render_to_response(
            'playlist.html',
            {
                'titlehead' : 'PlayIT - ' + playlist.name,
                'pagetitle' : 'View Playlist: ' + playlist.name,
                'playlist' : playlist,
                'tracks' : Track.objects.filter(playlist_track__in=Playlist_Track.objects.filter(id_playlist=playlist_id)),
                'pub' : playlist.id_pub
            }
        )

def get_playlist_tracks(request, playlist_id, format='html'):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        tracks = Track.objects.filter(playlist_track__in=Playlist_Track.objects.filter(id_playlist=playlist_id))
    except:
        raise Http404('Playlist not found.')
    if format == 'json':
        return render_json_response(tracks)
    elif format == 'xml':
        return render_xml_response(tracks)

def get_playlist_tracks_json(request, playlist_id):
    return get_playlist_tracks(request, playlist_id, 'json')

def get_playlist_tracks_xml(request, playlist_id):
    return get_playlist_tracks(request, playlist_id, 'xml')


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name = 'form.html'

class LoginRequiredCheckIsOwnerDeleteView(LoginRequiredMixin, CheckIsOwnerMixin, DeleteView):
    template_name = 'delete_form.html'
    success_url = "/"


class PubCreate(LoginRequiredMixin, CreateView):
    model = Pub
    template_name = 'form.html'
    form_class = PubForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PubCreate, self).form_valid(form)


class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'form.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.id_pub = Pub.objects.get(id=self.kwargs['pk'])
        return super(PlaylistCreate, self).form_valid(form)