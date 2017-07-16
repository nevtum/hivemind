from django.db import transaction
from django.utils import timezone

from api.core.domain.response import Success
from api.core.domain.user_stories import UserStory
from common import store as EventStore

from .. import constants
from ..models import Defect, Status


class CreateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        defect.submitter = request_object.user
        defect.save()
        event = self._create_event(defect)
        EventStore.append_next(event)
        return Success(defect)
    
    def _create_event(self, instance):
        return {
            'timestamp': instance.date_created,
            'sequence_nr': 0,
            'aggregate_id': instance.id,
            'aggregate_type': 'DEFECT',
            'event_type': constants.DEFECT_OPENED,
            'payload': {
                'project_code': instance.project_code,
                'release_id': instance.release_id,
                'priority': instance.priority.name,
                'reference': instance.reference,
                'description': instance.description,
                'comments': instance.comments
            },
            'owner': {
                'username': instance.submitter.username,
                'email': instance.submitter.email
            }
        }


class ImportDefectUserStory(UserStory):
    @transaction.atomic    
    def process_request(self, request_object):
        pass

class UpdateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        kwargs = self._to_kwargs(defect)
        model = defect.as_domainmodel()
        event = model.amend(request_object.user, timezone.now(), **kwargs)
        EventStore.append_next(event)
        defect.save()
        return Success(defect)

    def _to_kwargs(self, instance):
        return dict({
            'project_code': instance.project_code,
            'submitter': instance.submitter.username, # redundant field
            'release_id': instance.release_id,
            'status': instance.status.name, # redundant field. status is always open
            'priority': instance.priority.name,
            'reference': instance.reference,
            'description': instance.description,
            'comments': instance.comments,
        })

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
        pass

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