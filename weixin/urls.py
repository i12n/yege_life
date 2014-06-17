from django.conf.urls import patterns,url

from weixin import views

urlpatterns=patterns('',
	url(r'^check/$',views.check_signature1,name='check'),
	url(r'^index/$',views.index,name='index'),
)
