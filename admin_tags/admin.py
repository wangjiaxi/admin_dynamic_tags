from django.contrib import admin
from .models import Tag, TagBind, DynamicTag, TagItem
from .forms import TagInlineFormSet, SceneForm, TagForm
from django import forms
from django.contrib.contenttypes import admin as GA
from django.contrib.contenttypes.models import ContentType


class TagBindAdmin(admin.StackedInline):
    model = TagBind
    form = SceneForm
    min_num = 1
    extra = 0


class AttributeAdmin(admin.StackedInline):
    model = TagItem
    min_num = 1
    extra = 0


@admin.register(DynamicTag)
class DynamicTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias']
    inlines = [AttributeAdmin, TagBindAdmin]



class TagInline(GA.GenericTabularInline):

    model = Tag
    formset = TagInlineFormSet
    form = TagForm

    def tags_num(self):
        return len(TagBind.objects.get_d_tags_by_model(self.parent_model))

    def get_max_num(self, request, obj=None, **kwargs):
        return self.tags_num()

    def get_extra(self, request, obj=None, **kwargs):
        return self.tags_num()

    def has_add_permission(self, request):
        return False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(TagInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'd_tag':
            # limit the foreign key choices
            field.queryset = field.queryset.filter(id__in=TagBind.objects.get_d_tags_by_model(self.parent_model))
        return field
