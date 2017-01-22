from django.contrib import admin
from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image', 'date', 'id',]
    list_filter = ['date']


admin.site.register(Image, ImageAdmin)