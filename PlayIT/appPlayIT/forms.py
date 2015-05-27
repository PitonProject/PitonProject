from django.forms import ModelForm
from appPlayIT.models import Pub, Playlist, Track

class PubForm(ModelForm):
    class Meta:
        model = Pub
        exclude = ('user',)

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        exclude = ('pub', 'user')

class TrackForm(ModelForm):
    class Meta:
        model = Track
        #exclude = ()