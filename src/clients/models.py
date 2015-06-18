from django.db import models

titles = (
('Mr.', 'Mr.'),
('Mrs.', 'Mrs.'),
('Ms.', 'Ms.'))

class Contact(models.Model):
    employed_by = models.CharField(max_length=80)
    role = models.CharField(max_length=50)
    title = models.CharField(max_length=5, choices=titles)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

class Jurisdiction(models.Model):
    name = models.CharField(max_length=40)
    abbrev = models.CharField(max_length=10)
    regulator = models.CharField(max_length=40)

    def __str__(self):
        return '%s (%s)' % (self.abbrev, self.name)

class RecommendationSubscription(models.Model):
    user_id = models.ForeignKey('Contact')
    jurisdiction = models.ForeignKey('Jurisdiction')

    def __str__(self):
        return '[%s] %s' % (self.jurisdiction.abbrev, self.user_id)
