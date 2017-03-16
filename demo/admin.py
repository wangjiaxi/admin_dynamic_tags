from django.contrib import admin
from .models import Music, Album
from admin_tags.admin import TagInline


class MusicAdmin(admin.ModelAdmin):
    inlines = [TagInline]


class AlbumAdmin(admin.ModelAdmin):
    inlines = [TagInline]


admin.site.register(Music, MusicAdmin)
admin.site.register(Album, AlbumAdmin)
