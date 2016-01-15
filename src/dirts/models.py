from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Defect(models.Model):
    project_code = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    submitter = models.ForeignKey(User)
    release_id = models.CharField(max_length=50)
    status = models.ForeignKey(Status, default=1)
    priority = models.ForeignKey(Priority, default=1)
    reference = models.CharField(max_length=80)
    description = models.TextField()
    comments = models.TextField(blank=True)

    def is_active(self):
        return self.status.name != "Closed"

    def reopen(self, release_id):
        if self.status.name != "Closed":
            raise Exception("DIRT must be in closed state to reopen.")

        self.status = Status.objects.get(name='Open')
        self.release_id = release_id
        self.save()

    def close(self, release_id):
        self.status = Status.objects.get(name='Closed')
        self.release_id = release_id
        self.save()

class DefectHistoryItem(models.Model):
    date_created = models.DateTimeField()
    defect = models.ForeignKey(Defect)
    short_desc = models.CharField(max_length=80)
    submitter = models.ForeignKey(User)

    def __str__(self):
        return "[%s] %s" % (self.defect.project_code, self.short_desc)
