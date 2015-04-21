from django.shortcuts import render, render_to_response
from SpotifyAPI.spotify import SpotifyBrowser

# Create your views here.
def mainpage(request):
   return render_to_response(
        'mainpage.html',
        {
                'titlehead': 'PlayIT app',
                'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local',
                'user': request.user
        })

def browse_track(request, keyword, offset, limit):
    return render_to_response(
        'browse_track.html',
        {
            'titlehead' : 'PlayIT - Browse Track',
            'pagetitle' : 'Search a Track on Spotify',
            'user' : request.user,
            'keyword' : keyword,
            'tracks' : SpotifyBrowser.search_track(keyword, offset, limit)["tracks"]
        }
    )

def browse(request):
    type = request.GET.get('type')
    keyword = request.GET.get('keyword')
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 50)
    if not type or not keyword:
        return render_to_response(
            'browse.html',
            {
                    'titlehead': 'PlayIT - Browse',
                    'pagetitle': 'Benvingut a PlayIT. Una aplicacio de seleccio de musica per un local',
                    'user': request.user
            })
    else:
        if type == 'track':
            return browse_track(request, keyword, offset, limit)