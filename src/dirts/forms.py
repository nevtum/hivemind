from django.forms import ModelForm, Textarea
from dirts.models import Defect

class CreateDirtForm(ModelForm):
    class Meta:
        model = Defect
        fields = [
        'project_code',
        'release_id',
        'severity',
        'title',
        'description',
        'reference',
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80}),
            'reference': Textarea(attrs={'cols': 80}),
        }
