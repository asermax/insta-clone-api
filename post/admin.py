from django.contrib import admin
from . import models


class ImageInline(admin.TabularInline):
    model = models.Image


class PostAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)


admin.site.register(models.Post, PostAdmin)
