
from functools import reduce

from common.models import DomainEvent, Project
from dirts.models import Defect
from django.db.models import Q

from .response import Fail, Success


class UserStory(object):
    def execute(self, request_object):
        if request_object.is_valid():
            try:
                return self.process_request(request_object)
            except Exception as exc:
                return Fail.from_exception(exc)
        else:
            return Fail.from_invalid_request_object(request_object)
    
    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented")

class DomainEventFilterUserStory(UserStory):
    def process_request(self, request_object):
        req = request_object
        queryset = Defect.objects.all()
        if req.has_project_codes():
            code_query = reduce(lambda q, next: q | Q(project_code__iexact=next), req.projects, Q())
            queryset = queryset.filter(code_query)
        
        if req.has_search_string():
            to_q = create_map(req.search['q'])
            query = reduce(lambda q, next: q | to_q(next), req.search['search_on'], Q())
            queryset = queryset.filter(query)

        defect_ids = queryset.only('id').all()

        events = DomainEvent.objects.filter(
            aggregate_type='DEFECT',
            aggregate_id__in=defect_ids
        )
        events = events.select_related('owner')
        
        return Success(events)

def create_map(search_string):
    def to_q_object(property_name):
        item = {'{}__icontains'.format(property_name): search_string}
        return Q(**item)
    return to_q_object
