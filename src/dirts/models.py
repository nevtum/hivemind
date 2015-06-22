from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Defect(models.Model):
    project_code = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    submitter = models.ForeignKey(User)
    release_id = models.CharField(max_length=50)
    status = models.ForeignKey('Status')
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=2000)
    reference = models.CharField(max_length=1000)

    def __str__(self):
        return self.project_code
