from django.db import models
from django.db.models import Q


class ProjectsManager(models.Manager):
    def search(self, keyword):
        query = Q(description__icontains=keyword) \
            | Q(code__icontains=keyword)
        result_set = self.filter(query)
        return result_set.distinct()

class DomainEventManager(models.Manager):
    def belong_to(self, content_type, object_id):
        return self.filter(content_type=content_type, object_id=object_id)