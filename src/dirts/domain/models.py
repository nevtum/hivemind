from datetime import datetime

class Defect(object):
    """docstring for Defect"""
    def __init__(self, user_id, project_code, release):
        self.user_id = user_id
        self.project_code = project_code
        self.rel_status = ReleaseStatus(release, 'Open')
        self.date_created = datetime.now()

    def describe_symptom(self, reference, description):
        self.symptom = Symptom(reference, description)

    def update_comments(self, comments):
        self.comments = comments

    def update_status(self, release, status):
        self.rel_status = self.rel_status.change(release, status)

class Symptom(object):
    """docstring for """
    def __init__(self, reference, description):
        self.reference = reference
        self.description = description

class ReleaseStatus(object):
    """docstring for ReleaseStatus"""
    def __init__(self, release, status):
        self.release = release
        self.status = status

    def change(self, release, status):
        if self.release == release:
            if self.status != 'Open':
                raise Exception('Cannot change status!')
        else:
            if self.status != 'Closed':
                raise Exception('Cannot change release')

        return ReleaseStatus(release, status)
