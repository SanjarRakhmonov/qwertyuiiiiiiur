from django.conf.urls import url
from . import views 
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import login, logout, logout_then_login, password_reset, password_reset_done, password_reset_complete, password_reset_confirm 

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
	url(r'^logout-confirm/$', views.logout_confirm, name='logout_confirm'),
    #url(r'^edit/$', views.edit, name='edit'),
	 # login / logout urls
    #url(r'^login/$', views.user_login, name='login'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
	
	# change password urls
    #url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    #url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),

	# restore password urls
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
	
	
	#user profiles
    #url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),
	
	
	# urls for course application
    url(r'^enroll-course/$', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    url(r'^courses/$', views.StudentCourseListView.as_view(), name='student_course_list'),
	    url(r'^course/(?P<pk>\d+)/$',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'),
]
