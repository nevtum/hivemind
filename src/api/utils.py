# from dirts.models import Defect
# from common.models import Project, DomainEvent
# from django.db.models import Q

# def defect_activities(code, search_param):
#     defects = Defect.objects.all()
#     if code:
#         defects = defects.filter(project_code__iexact=code)
#     if search_param:
#         defects = defects.filter(
#             Q(reference__icontains=search_param) |
#             Q(description__icontains=search_param) |
#             Q(comments__icontains=search_param)
#         )
#     defect_ids = defects.only('id').all()

#     events = DomainEvent.objects.filter(
#         aggregate_type='DEFECT',
#         aggregate_id__in=defect_ids
#     )
#     events = events.select_related('owner')
#     return events

from .core.domain.user_stories import DomainEventFilterUserStory
from .core.domain.request import DomainEventListRequest

def defect_activities_new(code, search_param=''):
    story = DomainEventFilterUserStory()
    request_object = DomainEventListRequest.from_dict({
        'clients': [],
        'projects': [code],
        'usernames': [],
        'tags': {
            'match_all': [],
            'match_any': []
        },
        'search': {
            'q': search_param,
            'search_on': ['reference', 'description', 'comments']
        }
    })
    return story.execute(request_object)