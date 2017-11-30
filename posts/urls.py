from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^home', views.home, name='home'),
	url(r'^list/$', views.posts_list, name='list'),
	url(r'^detail/(?P<posts_slug>[-\w]+)/$', views.posts_detail, name="detail"),

	url(r'^create/$', views.posts_create, name='create'),
	url(r'^update/(?P<posts_slug>[-\w]+)/$', views.posts_update, name="update"),
	url(r'^delete/(?P<posts_slug>[-\w]+)/$', views.posts_delete, name="delete"),
	url(r'^ajax_like/(?P<post_id>\d+)/$', views.ajax_like, name="like_button"),

	url(r'^signup/$', views.usersignup, name="signup"),
	url(r'^login/$', views.userlogin, name="login"),
	url(r'^logout/$', views.userlogout, name="logout"), 
]
