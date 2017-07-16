class MutateDefectRequest(object):
    def __init__(self, user, form):
        self.form = form
        self.user = user
    
    def is_valid(self):
        if not hasattr(self, 'user') or not hasattr(self, 'form'):
            return False
        return self.form.is_valid()