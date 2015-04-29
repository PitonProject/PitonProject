from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from appPlayIT.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PlayIT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^$', mainpage, name='home'),
    url(r'^browse$', browse),
    url(r'^track/(\w+)/$', track),
    url(r'^pub/(\w+)/$', get_pub),
    url(r'^playlist/(\w+)/$', get_playlist)
)
