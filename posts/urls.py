# coding: utf-8

from django.conf.urls import url

from posts import views

urlpatterns = [
    url(r'^post/$', views.write, name='write'),
    url(r'^like/$', views.like, name='like'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^load/$', views.load, name='load'),
    url(r'^check/$', views.check, name='check'),
    url(r'^load_new/$', views.load_new, name='load_new'),
    url(r'^update/$', views.update, name='update'),
    url(r'^track_comments/$', views.track_comments, name='track_comments'),
    url(r'^remove/$', views.remove, name='remove_feed'),
    url(r'^remove-comment/$', views.remove_comment, name='remove_comment'),
    url(r'^(\d+)/$', views.feed, name='feed'),
]
