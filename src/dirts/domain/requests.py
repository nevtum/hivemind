class MutateDefectRequest(object):
    def __init__(self, user, form):
        self.form = form
        self.user = user
    
    def is_valid(self):
        if not hasattr(self, 'user') or not hasattr(self, 'form'):
            return False
        return self.form.is_valid()

class DeleteDefectRequest(object):
    def __init__(self, user, id):
        self.user = user
        self.id = id

    def is_valid(self):
        if not hasattr(self, 'user') or not hasattr(self, 'id'):
            return False
        return True

class SaveImportedDefectListRequest(object):
    def __init__(self, defects):
        self.defects = defects
    
    def is_valid(self):
        if not hasattr(self, 'defects'):
            return False
        return True