from .models import Defect

class DefectSearchMixin:
    """
    Mixin which combines with Defect ListView. Uses
    query_string_key as default but can be overridden in subclasses.
    """
    query_string_key = 'search'

    def get_queryset(self):
        keyword = self.request.GET.get(self.query_string_key, '')
        if not keyword:
            return super(DefectSearchMixin, self).get_queryset()

        return Defect.objects.search(keyword)