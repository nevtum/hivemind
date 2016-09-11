from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import Project

class Activity(models.Model):
    project = models.ForeignKey(Project)
    summary = models.CharField(max_length=80)
    date_occurred = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')