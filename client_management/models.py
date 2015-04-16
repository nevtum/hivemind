from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=20, primary_key=True, unique=True)
    status = ('Operational', 'Non-Operational')

    def __str__(self):
        return self.name

class Contact(models.Model):
    company = models.ForeignKey('Company')
    title = ('Mr.', 'Mrs.', 'Ms.')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
