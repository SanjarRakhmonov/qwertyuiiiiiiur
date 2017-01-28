"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site
from django.contrib.sitemaps.views import sitemap
from courses.views import CourseListView

from posts.views import actions_list, feeds

from core import views as core_views
from actions import views as activities_views
from search import views as search_views




urlpatterns = [
    url(r'^search/$', search_views.search, name='post_search'),
	url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^network/$', core_views.network, name='network'),
    url(r'^feeds/', include('posts.urls')),
	url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^$', core_views.home, name='home'),
	
    url(r'^course/', include('courses.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('user.urls')),
    url(r'^images/', include('images.urls', namespace='images')),
    url(r'^courses/$', CourseListView.as_view(), name='course_list'),
    url(r'^(?P<username>\w+)/$', core_views.profile, name='profile'),
    url(r'^(?P<username>\w+)/images/$', core_views.profile_images, name='profile_images'),
    url(r'^(?P<username>\w+)/followers/$', core_views.profile_followers, name='profile_followers'),
    url(r'^(?P<username>\w+)/following/$', core_views.profile_following, name='profile_following'),
	
    url(r'^hashtag/(?P<tag_slug>[-\w]+)/$', feeds, name='post_list_by_tag'),
	url('social-auth/', include('social.apps.django_app.urls', namespace='social')),

	
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	
