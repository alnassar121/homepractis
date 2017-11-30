from django.conf.urls import url
from api.views import *

urlpatterns = [
	url(r'^list/$', PostListAPIView.as_view(), name="list"),
	url(r'^detail/(?P<post_slug>[-\w]+)/$', PostDetailAPIView.as_view(), name="detail"),
	url(r'^delete/(?P<post_slug>[-\w]+)/$', PostDeleteAPIView.as_view(), name="delete"),
	url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
	url(r'^update/(?P<post_slug>[-\w]+)/$', PostUpdateAPIView.as_view(), name="update"),

	url(r'^comment/list/$', CommentListAPIView.as_view(), name="comment_list"),
	url(r'^comment/create/$', CommentCreateAPIView.as_view(), name="comment_create"),
	url(r'^register/$', UserCreateAPIView.as_view(), name="register"),
	url(r'^login/$', UserLoginAPIView.as_view(), name="login"),

]