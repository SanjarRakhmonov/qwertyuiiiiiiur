from django.contrib import admin
from .models import Feed


class FeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'hashtag_list', 'date', 'id')
    list_filter = ('date',)
    search_fields = ('post',)
	
    def get_queryset(self, request):
        return super(FeedAdmin, self).get_queryset(request).prefetch_related('tags')
    def hashtag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Feed, FeedAdmin)