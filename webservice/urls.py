from django.conf.urls import patterns, include, url
from django.contrib import admin
from  webservice import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webservice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/',  views.index, name='index'),
    url(r'^$',  views.index, name='index'),

    # Users
    url(r'^users/?$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),

    # Sites
    url(r'^sites/?$', views.site_list),
    url(r'^sites/(?P<pk>[0-9]+)/$', views.site_detail),

    # Clusters
    url(r'^clusters/?$', views.cluster_list),
    url(r'^clusters/(?P<pk>[0-9]+)/$', views.cluster_detail),

    # Hosts
    url(r'^hosts/?$', views.host_list),
    url(r'^hosts/(?P<pk>[0-9]+)/$', views.host_detail),

    # Softwares
    url(r'^softwares/?$', views.software_list),
    url(r'^softwares/(?P<pk>[0-9]+)/$', views.software_detail),

    # Scripts
    url(r'^scripts/?$', views.script_list),
    url(r'^scripts/(?P<pk>[0-9]+)/$', views.script_detail),

    # Events
    url(r'^events/?$', views.event_list),
    url(r'^events/(?P<pk>[0-9]+)/$', views.event_detail),
)
