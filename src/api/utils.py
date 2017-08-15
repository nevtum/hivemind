from .core.domain.user_stories import DomainEventFilterUserStory
from .core.domain.request import FilterListRequest
from common.models import Project

def defect_activities(project_code, search_param=''):
    story = DomainEventFilterUserStory()
    request_object = FilterListRequest.from_dict({
        'clients': [],
        'projects': projects_array(project_code),
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

def projects_array(project_code):
    if project_code == '':
        return []
    return [Project.objects.get(code=project_code).id]