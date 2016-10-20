from django.db import models

class SignupRequest(models.Model):
    pending_approval = models.BooleanField(default=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100)