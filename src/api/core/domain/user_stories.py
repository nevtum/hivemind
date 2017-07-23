from functools import reduce

from django.db.models import Q

from common.models import DomainEvent, Project
from common.utils import create_map
from dirts.models import Defect

from .response import Fail, Success


class UserStory(object):
    def execute(self, request_object):
        if request_object.is_valid():
            try:
                response = self.process_request(request_object)
                if response == None:
                    raise Exception("process_request did not return a reponse")
                return response
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
        if req.has_projects():
            queryset = queryset.filter(project__id__in=req.projects)
        
        if req.has_search_input():
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
