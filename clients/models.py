from django.db import models

# Create your models here.
stat = (('OP', 'Operational'), ('NOOP', 'Non-Operational'))

titles = (
('Mr.', 'Mr.'),
('Mrs.', 'Mrs.'),
('Ms.', 'Ms.'))

class Company(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=20, primary_key=True, unique=True)
    status = models.CharField(max_length=20, choices=stat, default='OP')

    def __str__(self):
        return self.name

class Contact(models.Model):
    company = models.ForeignKey('Company')
    title = models.CharField(max_length=5, choices=titles)
    role = models.ForeignKey('WorkRole')
    email = models.EmailField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

class WorkRole(models.Model):
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=20)

    def __str__(self):
        return self.name
