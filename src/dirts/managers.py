from django.db import models

class DefectsManager(models.Manager):
    def active(self):
        return self.latest().filter(status__name='Open')
    
    def latest(self):
        return self.order_by('-date_created')