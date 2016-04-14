from django.db import models
import uuid


def generate_uuid():
    return "%s" % (uuid.uuid4())


class Job(models.Model):
    name = models.CharField(max_length=100, blank=False, default=generate_uuid, unique=True)
    status = models.CharField(max_length=100, blank=False, default="created")
    command = models.TextField(blank=True, default="")
