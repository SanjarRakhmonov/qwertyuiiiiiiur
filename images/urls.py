from django.conf.urls import url
from . import views


urlpatterns = [
	url(r"^ajax-upload/$", views.ajax_uploader,name="ajax_uploader"),
	url(
        r'add/$',
        views.image_create,
        name='create'
    ),
    url(r'^like/$', views.like, name='image-like'),
    url(r'^comment/$', views.comment, name='image-comment'),
    url(r'^track_comments/$', views.track_comments, name='track_image_comments'),
    url(r'^detail/(?P<id>\d+)/$', views.image_detail, name='detail'),
    url(r'^$', views.image_list, name='list'),
]
#/taken-by=(?P<username>\w+)
