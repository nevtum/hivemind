class Success(object):
    def __init__(self, value):
        self.value = value
    
    @property
    def has_errors(self):
        return False

    def __repr__(self):
        return f"<Success({self.value})>"

class Fail(object):
    def __init__(self, message):
        self.message = message
    
    @property
    def has_errors(self):
        return True

    @classmethod
    def from_exception(cls, ex):
        errors = "\n".join(ex.args)
        return cls("{}: {}".format(ex.__class__.__name__, errors))

    @classmethod
    def from_invalid_request_object(cls, request_object):
        return cls(request_object.errors)
    
    def __repr__(self):
        return f"<Fail error={self.message}>"