from django.db import models

class DefectsManager(models.Manager):
    def active(self):
        return self.latest().filter(status__name='Open')
    
    def latest(self):
        return self.order_by('-date_created')
    
    def recently_changed(self):
        return self.order_by('-date_changed')
    
    def top_tags(self):
        try:
            return self.model.tags.most_common().order_by('-num_times', 'name')
        except:
            return None