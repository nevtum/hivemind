from collections import defaultdict

class FilterListRequest(object):
    def __init__(self, **adict):
        for key, value in adict.items():
            setattr(self, key, value)
        self.error_dict = defaultdict()

    def is_valid(self):
        self._validate_search_input()
        self._validate_tags_input()
        
        if self.error_dict:
            return False
        else:
            return True

    @property
    def errors(self):
        if self.error_dict:
            return self.error_dict

    @classmethod
    def from_dict(cls, adict):
        # rough validation
        return cls(**adict)

    def has_clients(self):
        if not hasattr(self, 'clients'):
            return False
        if self.clients == []:
            return False
        return True

    def has_projects(self):
        if not hasattr(self, 'projects'):
            return False
        if self.projects == []:
            return False
        for code in self.projects:
            if code != '':
                return True
        return False

    def has_search_input(self):
        if hasattr(self, 'search'):
            return True
        return False
    
    def _validate_search_input(self):
        if hasattr(self, 'search'):
            errors = []
            if 'q' not in self.search:
                errors.append("q string missing from search dictionary")
            if 'search_on' not in self.search:
                errors.append("search_on array missing from search dictionary")
            if len(errors) > 0:
                self.error_dict['search'] = errors
    
    def _validate_tags_input(self):
        if hasattr(self, 'tags'):
            errors = []
            if 'match_all' not in self.tags:
                errors.append("match_all array missing from tags dictionary")
            if 'match_any' not in self.tags:
                errors.append("match_any array missing from tags dictionary")
            if len(errors) > 0:
                self.error_dict['tags'] = errors