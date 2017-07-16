from django.db import transaction
from django.utils import timezone

from api.core.domain.response import Success
from api.core.domain.user_stories import UserStory
from common import store as EventStore

from ..models import Defect, Status
from ..utils import create_event_dto, create_payload


class CreateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        defect.submitter = request_object.user
        defect.save()
        event = create_event_dto(defect)
        EventStore.append_next(event)
        return Success(defect)

class ImportDefectUserStory(UserStory):
    @transaction.atomic    
    def process_request(self, request_object):
        raise NotImplementedError()

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
