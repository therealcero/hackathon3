from django.db import models

class Search(models.Model):
    name = models.CharField(max_length=255)
    articles = models.CharField(max_length=255)
    videos = models.CharField(max_length=1000)
    popularity = models.IntegerField()

class Chats(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    user = models.CharField(max_length=255)

class Req(models.Model):
    name = models.CharField(max_length=255)
    request = models.SmallIntegerField(default=0)
