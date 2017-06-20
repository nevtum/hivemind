from django.db import models
from django.db.models import Q


class DefectsManager(models.Manager):
    def get_queryset(self):
        qs = super(DefectsManager, self).get_queryset()
        return qs.select_related('status', 'priority', 'submitter')
        
    def active(self):
        return self.filter(status__name='Open')
    
    def recently_changed(self):
        return self.order_by('-date_changed')
    
    def top_tags(self):
        try:
            return self.model.tags.most_common().order_by('-num_times', 'name')
        except:
            return None
    
    def search(self, keyword):
        query = Q(reference__icontains=keyword) \
        | Q(project_code__icontains=keyword) \
        | Q(description__icontains=keyword) \
        | Q(comments__icontains=keyword) \
        | Q(release_id__icontains=keyword) \
        | Q(tags__name__in=[keyword])
        
        return self.filter(query).distinct()
