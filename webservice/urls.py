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

    # Files
    url(r'^files/?$', views.file_list),
    url(r'^set_file_content/(?P<pk>[0-9]+)/$', views.set_file_content),
    url(r'^put_local_file_to_hdfs/(?P<pk>[0-9]+)/(?P<hn>[0-9a-zA-Z]+)/$', views.put_local_file_to_hdfs),
    url(r'^pull_from_hdfs/(?P<pk>[0-9]+)/$', views.pull_from_hdfs),
    url(r'^download_file/(?P<pk>[0-9]+)/$', views.download_file),
    url(r'^set_file_content/(?P<pk>[0-9]+)/$', views.set_file_content),
    url(r'^files/(?P<pk>[0-9]+)/$', views.file_detail),

    # Jobs
    url(r'^jobs/?$', views.job_list),
    url(r'^jobs/(?P<pk>[0-9]+)/$', views.job_detail),
)
