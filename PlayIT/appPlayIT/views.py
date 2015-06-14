from django.shortcuts import render, render_to_response
from SpotifyAPI.spotify import SpotifyBrowser
from django.contrib.auth.models import User
from appPlayIT.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from appPlayIT.forms import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template import RequestContext

# Create your views here.
def mainpage(request):
    pubs = None
    if request.user.is_authenticated():
        pubs = Pub.objects.filter(user_pub__in=User_Pub.objects.filter(user=request.user))
    return render_to_response(
        'mainpage.html',
        {
                'user': request.user,
                'pubs' : pubs
        })

def browse_track(request, keyword, offset, limit, next_page, previous_page):
    return render_to_response(
        'browse_track.html',
        {
            'user': request.user,
            'keyword' : keyword,
            'tracks' : SpotifyBrowser.search_track(keyword, offset, limit)["tracks"],
            'next_page' : next_page,
            'previous_page': previous_page
        }
    )

def browse_artist(request, keyword, offset, limit, next_page, previous_page):
    return render_to_response(
        'browse_artist.html',
        {
            'user': request.user,
            'keyword' : keyword,
            'artists' : SpotifyBrowser.search_artist(keyword, offset, limit)["artists"],
            'next_page' : next_page,
            'previous_page' : previous_page
        }
    )

def browse_album(request, keyword, offset, limit, next_page, previous_page):
    return render_to_response(
        'browse_album.html',
        {
            'user': request.user,
            'keyword' : keyword,
            'albums' : SpotifyBrowser.search_album(keyword, offset, limit)["albums"],
            'next_page' : next_page,
            'previous_page' : previous_page
        }
    )

def browse_playlist(request, keyword, offset, limit, next_page, previous_page):
    return render_to_response(
        'browse_playlist.html',
        {
            'user': request.user,
            'keyword' : keyword,
            'playlists' : SpotifyBrowser.search_playlist(keyword, offset, limit)["playlists"],
            'next_page' : next_page,
            'previous_page' : previous_page
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
                    'user': request.user,
            })
    else:
        next_page = "/browse?keyword=" + keyword + "&type=" + type + "&limit=" + str(limit) + "&offset=" + str(offset+limit)
        previous_page = "/browse?keyword=" + keyword + "&type=" + type + "&limit=" + str(limit) + "&offset=" + str(offset-limit)
        if type == 'track':
            return browse_track(request, keyword, offset, limit, next_page, previous_page)
        elif type == 'artist':
            return browse_artist(request, keyword, offset, limit, next_page, previous_page)
        elif type == 'album':
            return browse_album(request, keyword, offset, limit, next_page, previous_page)
        elif type == 'playlist':
            return browse_playlist(request, keyword, offset, limit, next_page, previous_page)

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
                'user': request.user,
                'tracks' : tracks
            }
        )

def track(request, track_id):
    pubs = None
    pub_playlists = []
    if request.user.is_authenticated:
        pubs = Pub.objects.filter(user_pub__in=User_Pub.objects.filter(user=request.user))
        for pub in pubs:
            playlists = Playlist.objects.filter(pub = pub.id)
            if len(playlists) > 0:
                pub_playlists.append((pub, playlists))
    return render_to_response(
        'track.html',
        {
            'user' : request.user,
            'pubs' : pubs,
            'pub_playlists': pub_playlists,
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
                'user': request.user,
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
        user_follow_pub = 0 # User not authenticated
        user_is_owner = False
        if request.user.is_authenticated():
            if pub.user == request.user:
                user_is_owner = True
            try:
                user_pub = User_Pub.objects.get(user = request.user, pub = pub)
                user_follow_pub = 1 # User follow pub
            except:
                user_follow_pub = 2 # User authenticated, user don't follow pub
        reviews = Review.objects.filter(pub=pub_id)
        reviews_avg = None
        if reviews:
            reviews_avg = sum([int(rating[0]) for rating in reviews.values_list('rating')])/float(len(reviews))
        print reviews_avg
        return render_to_response(
            'pub.html',
            {
                'user': request.user,
                'pub' : pub,
                'user_follow_pub': user_follow_pub,
                'user_is_owner': user_is_owner,
                'playlists' : Playlist.objects.filter(pub=pub_id),
                'RATING_CHOICES' : Review.RATING_CHOICES,
                'reviews' : reviews,
                'reviews_avg' : reviews_avg,
                'number_of_reviews' : len(reviews)
            }, RequestContext(request)
        )

def get_pub_playlists_json(request, pub_id):
    return get_pub_playlists(request, pub_id, 'json')

def get_pub_playlists_xml(request, pub_id):
    return get_pub_playlists(request, pub_id, 'xml')

def get_pub_playlists(requests, pub_id, format='html'):
    try:
        pub = Pub.objects.get(id=pub_id)
        playlists = Playlist.objects.filter(pub=pub_id)
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
                'user': request.user,
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
        user_is_owner = False
        if request.user.is_authenticated():
            if playlist.user == request.user:
                user_is_owner = True
        return render_to_response(
            'playlist.html',
            {
                'user': request.user,
                'playlist' : playlist,
                'tracks' : Track.objects.filter(playlist_track__in=Playlist_Track.objects.filter(playlist=playlist_id)),
                'pub' : playlist.pub,
                'user_is_owner': user_is_owner
            }
        )

def get_playlist_tracks(request, playlist_id, format='html'):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        tracks = Track.objects.filter(playlist_track__in=Playlist_Track.objects.filter(playlist=playlist_id))
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
        form.instance.pub = Pub.objects.get(id=self.kwargs['pk'])
        return super(PlaylistCreate, self).form_valid(form)


@login_required()
def add_track_to_playlist(request, pk, pkr):
    try: # Track is already in playlist
        playlist_track = Playlist_Track.objects.get(playlist = pkr, track = pk)
        return HttpResponseRedirect("/playlist/" + str(pkr))
    except:
        pass
    playlist = get_object_or_404(Playlist, pk=pkr)
    track = None
    try:
        track = Track.objects.get(spotify_id = pk)
    except:
        spotify_track = SpotifyBrowser.get_track_by_id(pk)
        if "id" in spotify_track:
            print spotify_track["id"]
            track = Track(
                spotify_id = pk,
                name = spotify_track["name"],
                artist = spotify_track["artists"][0]["name"],
                album = spotify_track["album"]["name"]
            )
            track.save()
        else:
            raise Http404('Track not found.')
    new_playlist_track = Playlist_Track(
        playlist = playlist,
        track = track,
        user = request.user)
    new_playlist_track.save()
    return HttpResponseRedirect("/playlist/" + str(pkr))

@login_required()
def remove_track_from_playlist(request, pk, pkr):
    playlist_track = None
    try: # Track is already in playlist
        playlist_track = Playlist_Track.objects.get(playlist = pkr, track = pk)
    except:
        raise Http404('Track not found on this playlist!')
    if request.user == playlist_track.user:
        playlist_track.delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect("/playlist/" + str(pkr))

@login_required()
def follow_pub(request, pk):
    try:
        user_pub = User_Pub.objects.get(user = request.user, pub = pk)
    except:
        pub = get_object_or_404(Pub, id = pk)
        user_pub = User_Pub(user = request.user, pub = pub)
        user_pub.save()
    return HttpResponseRedirect("/pub/" + str(pk))

@login_required()
def unfollow_pub(request, pk):
    try:
        user_pub = User_Pub.objects.get(user = request.user, pub = pk)
        user_pub.delete()
    except:
        raise Http404('Pub not found on your follow list!')
    return HttpResponseRedirect("/pub/" + str(pk))

@login_required()
def review(request, pk):
    pub = get_object_or_404(Pub, pk=pk)
    new_review = Review(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        pub=pub)
    new_review.save()
    return HttpResponseRedirect("/pub/" + str(pk))