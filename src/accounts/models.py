from django.contrib.auth.models import User
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

    def reject(self):
        if not self.pending_approval:
            return

        self.pending_approval = False
        self.accepted = False
        self.save()

    
    def approve(self):
        if not self.pending_approval:
            return
        
        newuser = User()
        newuser.username = self.username
        newuser.first_name = self.first_name
        newuser.last_name = self.last_name
        newuser.email = self.email
        newuser.password = self.password
        newuser.save()

        self.pending_approval = False
        self.accepted = True
        self.save()
