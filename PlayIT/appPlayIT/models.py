from django.db import models

# Create your models here.
class Client(models.Model):
    userName = models.TextField(primary_key=True)
    password = models.TextField()
    name = models.TextField()
    surname = models.TextField(null=True)
    email = models.EmailField()


class Pub(models.Model):
    name = models.TextField()
    address = models.TextField()
    city = models.TextField()

class Client_Pub(models.Model):
    userName = models.ForeignKey(Client, primary_key=True)
    idPub = models.ForeignKey(Pub, primary_key=True)