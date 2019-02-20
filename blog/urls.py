from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from blog.models import Post


from .views import (
	post_create,
	post_update,
	post_delete,
	post_detail,
	post_list,
	#post_my_blog,
	contact,
	
	)


urlpatterns= [url(r'^$', post_list) ,
url(r'^(?P<id>\d+)$',  post_detail, name='detail'),
#url(r'^(?P<pk>\d+)$',  DetailView.as_view(model = Post, template_name ='blog/post.html'),name='detail'),
url(r'create/$', post_create),
#url(r'myblog/$', post_my_blog),
url(r'^(?P<id>\d+)/edit/$', post_update, name="update"),
url(r'^(?P<id>\d+)/delete/$', post_delete),
 url(r'^contact/', contact, name='contact'),
 
 ]


 #url(r'^$', ListView.as_view(queryset= Post.objects.all().order_by("-date")[:25],template_name="blog/blog.html"), name='list')
