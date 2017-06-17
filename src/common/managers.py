from django.db import models
from django.db.models import Q


class ProjectsManager(models.Manager):
    def search(self, keyword):
        query = Q(description__icontains=keyword) \
            | Q(code__icontains=keyword)
        result_set = self.filter(query)
        return result_set.order_by('-date_created').distinct()

class DomainEventManager(models.Manager):
    def belong_to(self, content_type, object_id):
        queryset = self.filter(content_type=content_type, object_id=object_id)
        return queryset.order_by('sequence_nr')