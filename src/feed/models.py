from django.db import models
from django.contrib.auth.models import User
from common.models import Project

class Activity(models.Model):
    project = models.ForeignKey(Project)
    summary = models.CharField(max_length=80)
    url = models.URLField()
    date_occurred = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User)