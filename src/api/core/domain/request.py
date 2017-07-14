
class DomainEventListRequest(object):
    def __init__(self, adict):
        for key, value in adict.items():
            setattr(self, key, value)
    
    def is_valid(self):
        return True

    @classmethod
    def from_dict(cls, adict):
        # rough validation
        return cls(adict)