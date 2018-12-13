from functools import reduce

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from api.core.domain.response import Success
from api.core.domain.user_stories import UserStory
from common import store as EventStore
from common.utils import create_map

from ..imports.serializers import ImportDefectSerializer
from ..models import Defect, Status
from ..utils import create_event_dto, create_import_event_dto, create_payload


class CreateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        defect.submitter = request_object.user
        defect.save()
        event = create_event_dto(defect)
        EventStore.append_next(event)
        return Success(defect)

class UpdateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        kwargs = create_payload(defect)
        model = defect.as_domainmodel()
        event = model.amend(request_object.user, timezone.now(), **kwargs)
        EventStore.append_next(event)
        defect.save()
        return Success(defect)

class CloseDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        form = request_object.form
        
        user = request_object.user
        release_id = form.cleaned_data['release_id']
        reason = form.cleaned_data['reason']
        date_closed = timezone.now()

        defect = form.save(commit=False)
        model = defect.as_domainmodel()
        event = model.close(user, release_id, reason, date_closed)
        EventStore.append_next(event)
        
        defect.status = Status.objects.get(name='Closed')
        defect.release_id = release_id
        defect.save()
        return Success(defect)

class ReopenDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        form = request_object.form
        release_id = form.cleaned_data['release_id']
        reason = form.cleaned_data['reason']

        defect = form.save(commit=False)
        model = defect.as_domainmodel()
        event = model.reopen(request_object.user, release_id, reason, timezone.now())
        EventStore.append_next(event)
        defect.status = Status.objects.get(name='Open')
        defect.release_id = release_id
        defect.save()
        return Success(defect)

class DeleteDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = Defect.objects.get(pk=request_object.id)
        model = defect.as_domainmodel()
        event = model.soft_delete(request_object.user, timezone.now())
        EventStore.append_next(event)
        defect.delete()
        return Success(None)

class LockDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        form = request_object.form
        defect = form.instance
        defect_model = defect.as_domainmodel()
        event = defect_model.make_obsolete(
            user=request_object.user,
            timestamp=timezone.now(),
            **form.cleaned_data
        )
        EventStore.append_next(event)
        return Success(defect)

class CommitImportDefectListUserStory(UserStory):
    @transaction.atomic    
    def process_request(self, request_object):
        for json in request_object.defects:
            if json['status'] == 'Closed':
                self.persist_closed_defect(json)
            else:
                self.persist_open_defect(json)
        return Success(None)
    
    def persist_open_defect(self, json_data):
        serializer = ImportDefectSerializer(data=json_data)
        if not serializer.is_valid():
            raise Exception("Something went wrong with import!")
        defect = serializer.save()
        event = create_import_event_dto(defect)
        EventStore.append_next(event)
        return defect

    def persist_closed_defect(self, json_data):
        updated_data = json_data.copy()
        updated_data['status'] = 'Open'
        date_closed = self.get_closed_date(updated_data)
        defect = self.persist_open_defect(updated_data)
        user = defect.submitter
        release_id = defect.release_id
        model = defect.as_domainmodel()
        event = model.close(user, release_id, '', date_closed)
        EventStore.append_next(event)
        defect.status = Status.objects.get(name='Closed')
        defect.release_id = release_id
        defect.save()

    def get_closed_date(self, json_data):
        serializer = ImportDefectSerializer(data=json_data)
        if serializer.is_valid():
            return serializer.validated_data['date_changed']

class FilterDefectListUserStory(UserStory):
    def process_request(self, request_object):
        req = request_object
        queryset = Defect.objects.all()

        if req.has_clients():
            queryset = queryset.filter(project__manufacturer__id__in=req.clients)

        if req.has_projects():
            queryset = queryset.filter(project__id__in=req.projects)
        
        if req.has_search_input():
            to_q = create_map(req.search['q'])
            query = reduce(lambda q, next: q | to_q(next), req.search['search_on'], Q())
            queryset = queryset.filter(query)
        
        return Success(queryset)
