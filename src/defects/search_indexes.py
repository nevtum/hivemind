from haystack import indexes
from .models import Defect

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='reference')
    code = indexes.CharField(model_attr='project_code')
    body = indexes.CharField(model_attr='description')
    comments = indexes.CharField(model_attr='comments')

    def get_model(self):
        return Defect

    def index_queryset(self, using=None):
        return self.get_model().objects.all()