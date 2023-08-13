from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        'username', 'first_name', 'last_name',
        'password', 'avatar'
    ]


@admin.register(models.Podcast)
class PodcastAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    ...
