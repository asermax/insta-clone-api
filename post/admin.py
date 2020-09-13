from django.contrib import admin
from . import models


class ImageInline(admin.TabularInline):
    model = models.Image


class CommentInline(admin.TabularInline):
    model = models.Comment


class PostAdmin(admin.ModelAdmin):
    inlines = (ImageInline, CommentInline)


admin.site.register(models.Post, PostAdmin)
