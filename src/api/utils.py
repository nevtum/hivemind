from .core.domain.user_stories import DomainEventFilterUserStory
from .core.domain.request import FilterListRequest

def defect_activities(code, search_param=''):
    story = DomainEventFilterUserStory()
    request_object = FilterListRequest.from_dict({
        'clients': [],
        'projects': [code],
        'usernames': [],
        'search': {
            'q': search_param,
            'search_on': ['reference', 'description', 'comments']
        }
    })
    response = story.execute(request_object)
    if response.has_errors:
        raise ValueError(response.message)
    return response.value