from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Severity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Defect(models.Model):
    project_code = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    submitter = models.ForeignKey(User)
    release_id = models.CharField(max_length=50)
    status = models.ForeignKey(Status, default=1)
    severity = models.ForeignKey(Severity, default=1)
    title = models.CharField(max_length=80)
    description = models.TextField()
    reference = models.TextField(default='N/A')

    def __str__(self):
        return self.project_code
