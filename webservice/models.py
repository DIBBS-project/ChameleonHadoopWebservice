from django.db import models
import uuid


class File(models.Model):
    name = models.CharField(max_length=100, blank=False, default="%s" % (uuid.uuid4()), unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    local_file_path = models.CharField(max_length=100, blank=False, default="%s" % (uuid.uuid4()))
    hdfs_name = models.CharField(max_length=100, blank=False, default="%s" % (uuid.uuid4()), unique=True)
    # data = models.FileField()


class Job(models.Model):
    name = models.CharField(max_length=100, blank=False, default="%s" % (uuid.uuid4()), unique=True)
    # start_date = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, to_field='id')
    status = models.CharField(max_length=100, blank=False, default="created")
