from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
import sites
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yege_life.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
	url(r'^weixin/',include('weixin.urls')),
	url(r'^sites/',include('sites.urls')),
)#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
