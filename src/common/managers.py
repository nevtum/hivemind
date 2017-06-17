from django.db import models
from django.db.models import Q


class ProjectsManager(models.Manager):
    def search(self, keyword):
        query = Q(description__icontains=keyword) \
            | Q(code__icontains=keyword)
        result_set = self.filter(query)
        return result_set.order_by('-date_created').distinct()

class DomainEventManager(models.Manager):
    def belong_to(self, agg_type, agg_id):
        queryset = self.filter(aggregate_type=agg_type, aggregate_id=agg_id)
        return queryset.order_by('sequence_nr')