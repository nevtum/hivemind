from collections import defaultdict

class DomainEventListRequest(object):
    def __init__(self, adict):
        self.error_dict = defaultdict()
        for key, value in adict.items():
            setattr(self, key, value)
    
    def has_project_codes(self):
        if self.projects == []:
            return False
        for code in self.projects:
            if code != '':
                return True
        return False

    def has_search_string(self):
        if self.search['q'] != '':
            return True
        else:
            return False

    def is_valid(self):
        self._validate_search_input()
        self._validate_tags_input()
        
        if self.error_dict:
            return False
        else:
            return True
    
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

    @property
    def errors(self):
        if self.error_dict:
            return self.error_dict

    @classmethod
    def from_dict(cls, adict):
        # rough validation
        return cls(adict)