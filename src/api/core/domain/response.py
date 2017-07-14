class Success(object):
    def __init__(self, value):
        self.value = value

class Fail(object):
    def __init__(self, message):
        self.value = message
    
    @classmethod
    def from_exception(cls, ex):
        errors = "\n".join(ex.args)
        return cls("{}: {}".format(ex.__class__.__name__, errors))

    @classmethod
    def from_invalid_request_object(cls, request_object):
        return cls(request_object.errors)