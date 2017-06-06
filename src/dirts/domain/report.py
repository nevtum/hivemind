
from django.shortcuts import get_object_or_404

from common.models import Project

from ..models import Defect


def _to_dto(index, defect, freeze_date):
    defect_model = defect.as_domainmodel(freeze_date)
    owner = '{} {}'.format(defect.submitter.first_name, defect.submitter.last_name)
    if defect_model.status == 'Open':
        status = 'Active'
    else:
        status = 'Closed'
        
    return {
        'id': index + 1001,
        'version': defect_model.release_id,
        'reference': defect_model.reference,
        'date_logged': defect_model.date_created,
        'level': defect_model.priority,
        'owner': owner,
        'description': defect_model.description,
        'comments': defect_model.comments,
        'status': status
    }

def defect_summary(project_code, freeze_date, show_active=True):
    project = get_object_or_404(Project, code=project_code)
    queryset = Defect.objects.filter(
        project_code=project_code,
        date_created__lte=freeze_date
        ).order_by('date_created')
    items = [_to_dto(index, defect, freeze_date) for index, defect in enumerate(queryset)]

    if show_active:
        return project, filter(lambda x: x['status'] == 'Active', items)
    else:
        return project, items
