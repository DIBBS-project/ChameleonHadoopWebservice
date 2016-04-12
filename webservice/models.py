from django.db import models
import uuid


def generate_uuid():
    return "%s" % (uuid.uuid4())


class File(models.Model):
    name = models.CharField(max_length=100, blank=False, default=generate_uuid, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    local_file_path = models.CharField(max_length=100, blank=False, default=generate_uuid)
    hdfs_name = models.CharField(max_length=100, blank=False, default=generate_uuid, unique=True)
    # data = models.FileField()


class Job(models.Model):
    name = models.CharField(max_length=100, blank=False, default=generate_uuid, unique=True)
    # start_date = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, to_field='id')
    status = models.CharField(max_length=100, blank=False, default="created")
    parameters = models.TextField(blank=True, default="")
