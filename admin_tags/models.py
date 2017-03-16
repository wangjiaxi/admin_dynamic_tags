from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from smart_selects.db_fields import ChainedManyToManyField


@python_2_unicode_compatible
class DynamicTag(models.Model):
    class Meta:
        verbose_name = _("Dynamic Tag")
        verbose_name_plural = _("Dynamic Tags")

    name = models.CharField(verbose_name=_('Name'),  max_length=100)
    alias = models.CharField(verbose_name=_('Alias'), max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TagItem(models.Model):
    class Meta:
        verbose_name = _("Tag Item")
        verbose_name_plural = _("Tag Items")

    d_tag = models.ForeignKey(DynamicTag, verbose_name=_("Dynamic Tag"),
                              related_name="%(app_label)s_%(class)s_d_tag")
    key = models.CharField(verbose_name=_("Key"), max_length=100)

    def __str__(self):
        return self.key


class TagBindManager(models.Manager):

    def get_d_tags_by_model(self, model=None):
        return self.filter(model=ContentType.objects.get_for_model(model)).values('d_tag')


@python_2_unicode_compatible
class TagBind(models.Model):
    """limited the models used by DynamicTag, same as DynamicTag permissions"""
    class Meta:
        verbose_name = _("Tag Bind")
        verbose_name_plural = _("Tag Bind")
    d_tag = models.ForeignKey(DynamicTag, verbose_name=_("Dynamic Tag"),
                              related_name="%(app_label)s_%(class)s_d_tag")
    model = models.ForeignKey(ContentType, verbose_name=_("Model"),
                              help_text=_("What model would use this tag?"),
                              related_name="%(app_label)s_%(class)s_model")

    objects = TagBindManager()

    def __str__(self):
        return self.d_tag.name


class TagManager(models.Manager):

    def values(self, instance):
        tags = self.get_tag_list(instance=instance)
        context = []
        for tag in tags:
            context.append({
                'tag': tag.d_tag,
                'values': tag.value.get_queryset(),
             })
        return context

    def values_to_dict(self, instance):
        tags = self.get_tag_list(instance=instance)
        context = []
        for tag in tags:
            context.append({
                'tag': tag.d_tag.name,
                'values': [t.key for t in tag.value.get_queryset()],
             })
        return context

    def get_tag_list(self, instance):
        return self.filter(content_type=ContentType.objects.get_for_model(instance),
                           object_id=instance.pk)


@python_2_unicode_compatible
class Tag(models.Model):
    """
      ```
      from django.contrib.contenttypes.generic import GenericRelation

      class Music(models.Model):
          name = models.CharField(max_length=20)
          album = models.ForeignKey(Album)
          tags = GenericRelation(Tag)

          def __str__(self):
              return self.name

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

      # Get tags by instance
      >>> Tag.objects.values(music)
      ...
        [{'tag': <DynamicTag: Color>, 'values': [<TagItem: Yellow>]},
         {'tag': <DynamicTag: Type>, 'values': [<TagItem: Smart>, <TagItem: Simple>]}]

      >>> Tag.objects.values_to_dict(music)
      ...
        [{'tag': 'Color', 'values': ['Yellow']},
         {'tag': 'Type', 'values': ['Smart', 'Simple']}]

      ```
    """
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tag")
        unique_together = ("content_type", "object_id", "d_tag")

    content_type = models.ForeignKey(ContentType, verbose_name=_("Model Type"),
                                     related_name="%(app_label)s_%(class)s_content_type")
    object_id = models.CharField(verbose_name=_("Object Id"), max_length=100)
    content = GenericForeignKey("content_type", "object_id")
    d_tag = models.ForeignKey(DynamicTag, verbose_name=_("Dynamic Tag"),
                              related_name="%(app_label)s_%(class)s_d_tag")
    value = ChainedManyToManyField(
        TagItem,
        verbose_name=_("Value"),
        chained_field="d_tag",
        chained_model_field="d_tag",
        blank=True,
    )

    objects = TagManager()

    def __str__(self):
        return self.d_tag.name
