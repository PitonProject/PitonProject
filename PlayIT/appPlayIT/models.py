from django.db import models

# Create your models here.
class Client(models.Model):
    username = models.TextField(primary_key=True)
    #password = models.TextField()
    name = models.TextField()
    surname = models.TextField(null=True)
    email = models.EmailField()

class Pub(models.Model):
    id_spotify_user = models.TextField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    city = models.TextField()

class Client_Pub(models.Model):
    id_client = models.ForeignKey(Client, primary_key=True)
    id_pub = models.ForeignKey(Pub, primary_key=True)

class Playlist(models.Model):
    id_spotify_playlist = models.TextField(primary_key=True)
    id_pub = models.ForeignKey(Pub)

