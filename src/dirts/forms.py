from django.forms import ModelForm, Textarea
from dirts.models import Defect

class CreateDirtForm(ModelForm):
    class Meta:
        model = Defect
        fields = [
        'project_code',
        'release_id',
        'priority',
        'reference',
        'description',
        'comments',
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80}),
            'comments': Textarea(attrs={'cols': 80}),
        }
