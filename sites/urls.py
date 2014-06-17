from django.conf.urls import patterns, include, url
from sites import views
urlpatterns = patterns('',
  
  
	url(r'^(?P<username>\w+)/get/',views.get_news,name='show'),
	url(r'^(?P<username>\w+)/show/',views.index,name='read'),  
  
)
