from django.db import models
from django.contrib.auth.models import User

#class Client(models.Model):
 #   username = models.TextField(primary_key=True)
  #  password = models.TextField()
   # name = models.TextField()
    #surname = models.TextField(null=True)
    #email = models.EmailField()

class Pub(models.Model):
    #id_spotify_user = models.TextField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    city = models.TextField()
    #id_owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

#class Client_Pub(models.Model):
 #   id_client = models.ForeignKey(Client, primary_key=True)
  #  id_pub = models.ForeignKey(Pub, primary_key=True)

class User_Pub(models.Model):
    id_user = models.ForeignKey(User)
    id_pub = models.ForeignKey(Pub)
    class Meta:
        unique_together = ('id_user', 'id_pub')

class Playlist(models.Model):
    #id_spotify_playlist = models.TextField(primary_key=True)
    id_pub = models.ForeignKey(Pub, related_name='playlists')
    name = models.TextField()
    def __unicode__(self):
        return self.name

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