from django.db import models
from django.contrib.contenttypes.generic import GenericRelation
from admin_tags.models import Tag


class Album(models.Model):
    name = models.CharField(max_length=20)
    tags = GenericRelation(Tag)

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=20)
    album = models.ForeignKey(Album)
    tags = GenericRelation(Tag)

    def __str__(self):
        return self.name
