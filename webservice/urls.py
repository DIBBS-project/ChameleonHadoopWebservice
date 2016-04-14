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
    # url(r'^files/?$', views.file_list),
    # url(r'^files/(?P<pk>[0-9]+)/$', views.file_detail),
    #
    # url(r'^set_file_content/(?P<pk>[0-9]+)/$', views.set_file_content),
    # url(r'^put_local_file_to_hdfs/(?P<pk>[0-9]+)/(?P<hn>[0-9a-zA-Z]+)/$', views.put_local_file_to_hdfs),
    # url(r'^pull_from_hdfs/(?P<pk>[0-9]+)/$', views.pull_from_hdfs),
    # url(r'^download_file/(?P<pk>[0-9]+)/$', views.download_file),

    # FS Files
    url(r'^fs/ls/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.fs_file_detail),
    url(r'^fs/ls//$', views.fs_file_detail),
    url(r'^fs/mkdir/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.create_fs_folder),
    url(r'^fs/rm/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.fs_delete_file),
    url(r'^fs/rmdir/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.fs_delete_folder),
    url(r'^fs/upload/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.upload_fs_file),
    url(r'^fs/download//(?P<path>[0-9a-zA-Z/_.-]+)/$', views.download_fs_file),

    # HDFS Files
    url(r'^hdfs/ls/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.hdfs_file_detail),
    url(r'^hdfs/ls//$', views.hdfs_file_detail),
    url(r'^hdfs/mkdir/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.create_hdfs_folder),
    url(r'^hdfs/rm/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.hdfs_delete_file),
    url(r'^hdfs/rmdir/(?P<path>[0-9a-zA-Z/_.-]+)/$', views.hdfs_delete_folder),
    url(r'^hdfs/upload/(?P<hdfspath>[0-9a-zA-Z/_.-]+)/$', views.upload_hdfs_file),
    url(r'^hdfs/download/(?P<hdfspath>[0-9a-zA-Z/_.-]+)/$', views.download_hdfs_file),

    # Jobs
    url(r'^jobs/?$', views.job_list),
    url(r'^jobs/(?P<pk>[0-9]+)/$', views.job_detail),
    url(r'^run_hadoop_job/(?P<pk>[0-9]+)/$', views.run_hadoop_job),
    url(r'^get_running_jobs/$', views.get_running_jobs),
)
