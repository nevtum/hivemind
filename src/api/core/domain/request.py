
class DomainEventListRequest(object):
    def __init__(self, adict):
        for key, value in adict.items():
            setattr(self, key, value)
    
    def has_project_codes(self):
        if self.projects == []:
            return False
        for code in self.projects:
            if (code != '') and (code != None):
                return True
        return False

    def has_search_string(self):
        if self.search['q'] != '':
            return True
        else:
            return False

    def is_valid(self):
        expected_props = ['clients', 'projects', 'usernames', 'tags', 'search']
        for prop_name in expected_props:
            if not hasattr(self, prop_name):
                return False
        return True

    @classmethod
    def from_dict(cls, adict):
        # rough validation
        return cls(adict)