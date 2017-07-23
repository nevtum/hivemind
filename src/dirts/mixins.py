from django.shortcuts import get_object_or_404

from api.core.domain.request import FilterListRequest
from common.models import CustomFilter

from .domain.user_stories import FilterDefectListUserStory
from .models import Defect


# class DefectSearchMixin:
#     """
#     Mixin which combines with Defect ListView. Uses
#     query_string_key as default but can be overridden in subclasses.
#     """
#     query_string_key = 'search'

#     def get_queryset(self):
#         keyword = self.request.GET.get(self.query_string_key, '')
#         if not keyword:
#             return super(DefectSearchMixin, self).get_queryset()

#         return Defect.objects.search(keyword)

class FilterListMixin(object):
    def get_queryset(self):
        keyword = self.request.GET.get('search', '')
        slug_name = self.kwargs.get('slug', '')
        if keyword or slug_name:
            adict = {}
            if keyword:
                adict['search'] = {
                    'q': keyword,
                    'search_on': [
                        'reference',
                        'project_code',
                        'description',
                        'comments',
                        'release_id'
                    ]
                }

            if slug_name:
                custom_filter = get_object_or_404(CustomFilter, slug=slug_name)
                clients = [cl.id for cl in custom_filter.clients.all()]
                projects = [pr.id for pr in custom_filter.projects.all()]
                users = [u.id for u in custom_filter.users.all()]
                tags = [t.id for t in custom_filter.tags.all()]
                if clients:
                    adict['clients'] = clients
                if projects:
                    adict['projects'] = projects
                if users:
                    adict['users'] = users
                if tags:
                    adict['tags'] = {
                        'match_all': tags,
                        'match_any': []
                    }
            request_object = FilterListRequest().from_dict(adict)
            response = FilterDefectListUserStory().execute(request_object)
            if response.has_errors:
                raise ValueError(response.message)
            return response.value
        else:
            return super(FilterListMixin, self).get_queryset()
