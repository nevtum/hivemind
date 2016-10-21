from django.db import models

class SignupRequest(models.Model):
    pending_approval = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100)