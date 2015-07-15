from dirts.domain.models import Defect, Symptom, DefectState
from dirts.models import Defect as DIRT
from dirts.models import Priority, Status, DefectHistoryItem

def get_defect(id):
    dto = DIRT.objects.get(pk=id)
    state = DefectState(dto.release_id, dto.status.name)
    defect = Defect(dto.submitter, dto.project_code, state)
    defect.describe_symptom(dto.reference, dto.description, dto.priority.name)
    defect.update_comments(dto.comments)
    return defect

def save(defect):
    pass
