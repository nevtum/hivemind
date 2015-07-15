from datetime import datetime

class Defect(object):
    """docstring for Defect"""
    def __init__(self, user_id, project_code, initial_state):
        self.user_id = user_id
        self.project_code = project_code
        self.state = initial_state
        self.date_created = datetime.now()

    def describe_symptom(self, reference, description, priority):
        self.symptom = Symptom(reference, description, priority)

    def update_comments(self, comments):
        self.comments = comments

    def update_state(self, release, status):
        self.state = self.state.change(release, status)

class Symptom(object):
    """docstring for """
    def __init__(self, reference, description, priority):
        self.reference = reference
        self.description = description
        self.priority = priority

class DefectState(object):
    """docstring for DefectState"""
    def __init__(self, release, status='Open'):
        self.release = release
        self.status = status

    def change(self, release, status):
        if self.release == release:
            if self.status != 'Open':
                raise Exception('Cannot change status!')

        return DefectState(release, status)
