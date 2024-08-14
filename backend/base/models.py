from django.db import models


class AnonymousPerson(models.Model):
  name = models.CharField(max_length=100)


class Person(AnonymousPerson):
  email = models.EmailField()
  picture = models.URLField()
  

class AnonymousGuest(AnonymousPerson):
  pass


class Guest(Person):
  pass


class Host(Person):
  pass


class HistoryPieces(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  
  
class History(models.Model):
  pieces = models.ManyToManyField(HistoryPieces)


class HostSet(models.Model):
  hosts = models.ManyToManyField(Host)
  history = models.ForeignKey(History)


class Gift(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  value = models.FloatField()
  picture = models.URLField()


class Event(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(max_length=500)
  hostset = models.ForeignKey(HostSet)
  guests = models.ManyToManyField(Host)
  gifts = models.ManyToManyField(Gift)

  