from django.db import models
from django.contrib.auth.models import User

class Pub(models.Model):
    name = models.TextField()
    street = models.TextField()
    number = models.TextField()
    city = models.TextField()
    zipCode = models.TextField(blank=True, null=True)
    stateOrProvince = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/pub/" + str(self.pk)

class User_Pub(models.Model):
    id_user = models.ForeignKey(User)
    id_pub = models.ForeignKey(Pub)
    class Meta:
        unique_together = ('id_user', 'id_pub')

class Playlist(models.Model):
    id_pub = models.ForeignKey(Pub, related_name='playlists')
    name = models.TextField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/playlist/" + str(self.pk)

class Track(models.Model):
    spotify_id = models.TextField(primary_key=True)
    name = models.TextField()
    artist = models.TextField()
    #spotify_artist_id = models.TextField()
    album = models.TextField()
    #spotify_album_id = models.TextField()
    def __unicode__(self):
        return self.name + " - " + self.artist

class Playlist_Track(models.Model):
    id_playlist = models.ForeignKey(Playlist)
    id_track = models.ForeignKey(Track)
    id_user = models.ForeignKey(User)
    class Meta:
        unique_together = ('id_playlist', 'id_track')