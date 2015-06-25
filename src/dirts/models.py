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
        return str(self.date_created)

    def is_active(self):
        return self.status.name != "Closed"

class DefectHistoryItem(models.Model):
    date_created = models.DateTimeField()
    defect = models.ForeignKey(Defect)
    short_desc = models.CharField(max_length=80)
    submitter = models.ForeignKey(User)

    def __str__(self):
        return "[%s] %s" % (self.defect.project_code, self.short_desc)
