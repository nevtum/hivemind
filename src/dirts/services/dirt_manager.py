from django.db.models import Q
from dirts.models import Defect
from common import store as EventStore

def latest_dirts(keyword):
    if not keyword:
        return Defect.objects.latest()
    
    query = Q(reference__icontains=keyword) \
    | Q(project_code__icontains=keyword) \
    | Q(description__icontains=keyword) \
    | Q(comments__icontains=keyword) \
    | Q(release_id__icontains=keyword) \
    | Q(tags__name__in=[keyword])

    return Defect.objects.latest().filter(query)    

def delete_dirt(dirt_id, user):
    defect = Defect.objects.get(pk=dirt_id).as_domainmodel()
    event = defect.soft_delete(user)
    EventStore.append_next(event)
    
    Defect.objects.get(id=dirt_id).delete()