# Django admin_dynamic_tags

Django `admin_dynamic_tags` is convenient tags management system.
You can bind the tag to different model, and one model could use
multiple tags. You can add tags by django admin site also use django
queryset.

### Add tags in your models

```
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


```
Then you can use the API like so:

      >>>music = Music.objects.first()
      >>>music.tags.all()
      ... [<Tag: Color>, <Tag: Type>]
      >>> color, _type = music.tags.all()
      >>> color.value.get_queryset()
      ...[<TagItem: Yellow>]
      >>>  type.value.get_queryset()
      ... [<TagItem: Smart>, <TagItem: Simple>]
      >>> smart.key
      ... Smart

Get tags by instance

     >>> Tag.objects.values(music)
     ... [{'tag': <DynamicTag: Color>, 'values': [<TagItem: Yellow>]},
         {'tag': <DynamicTag: Type>, 'values': [<TagItem: Smart>, <TagItem: Simple>]}]

     >>> Tag.objects.values_to_dict(music)
     ...[{'tag': 'Color', 'values': ['Yellow']},{'tag': 'Type', 'values': ['Smart', 'Simple']}]


### Add tags by django admin site, need two steps merely.

- First create dynamic tags, add tag's name , tag's items. and select what tags had permission use this tags


![](http://upload-images.jianshu.io/upload_images/1803273-8fd7d125b3cd0f39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- Select instance and edit the tags.

![](http://upload-images.jianshu.io/upload_images/1803273-1d49ca5e638a20ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### How to use this app
- add     'admin_tags', 'smart_selects' in INSTALLED_APPS / settings.py
- url(r'^chaining/', include('smart_selects.urls')) in your urls.py

