from django.db import models

class Search(models.Model):
    name = models.CharField(max_length=255)
    articles = models.CharField(max_length=255)
    videos = models.CharField(max_length=1000)
    popularity = models.IntegerField()
