from django.db import models
import uuid


def generate_uuid():
    return "%s" % (uuid.uuid4())


class Job(models.Model):
    name = models.CharField(max_length=100, blank=False, default=generate_uuid)
    status = models.CharField(max_length=100, blank=False, default="created")
    command = models.TextField(blank=True, default="")


class Execution(models.Model):
    application_hadoop_id = models.CharField(max_length=100, blank=False, default=generate_uuid, unique=True)
    job = models.ForeignKey(Job, to_field='id')