from django import forms
from django.forms import ModelForm, Textarea
from django.utils import timezone

from .constants import CANNOT_REPRODUCE, DO_NOT_FIX, RAISED_IN_ERROR, RESOLVED
from .models import Defect


class DefectSummaryForm(ModelForm, forms.Form):
    prior_to_date = forms.DateField(initial=timezone.now)
    show_active_only = forms.BooleanField(required=False, initial=True)
    
    class Meta:
        model = Defect
        fields = [
            'project_code'
        ]

class TagsForm(ModelForm):
    class Meta:
        model = Defect
        fields = [
            'tags'
        ]

class CreateDefectForm(ModelForm):
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

class ReopenDefectForm(ModelForm, forms.Form):
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Defect
        fields = [
            'release_id',
        ]

CLOSE_REASONS = (
    ('', '<select reason>'),
    (CANNOT_REPRODUCE, 'Could not reproduce'),
    (RAISED_IN_ERROR, 'Raised in error'),
    (DO_NOT_FIX, 'Do not fix'),
    (RESOLVED, 'Resolved'),
)

class CloseDefectForm(ModelForm, forms.Form):
    reason = forms.ChoiceField(choices = CLOSE_REASONS)
    details = forms.CharField(widget=forms.Textarea, required=False)
        
    class Meta:
        model = Defect
        fields = [
            'release_id',
        ]
    
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['details'] != '':
            cleaned_data['reason'] += "\n\n{}".format(cleaned_data['details'])
        return cleaned_data

LOCK_REASONS = (
    ('', '<select reason>'),
    ('Invalid issue raised.', 'Invalid issue raised'),
    ('Backlogged for future releases.', 'Backlogged for future releases'),
    ('No longer valid: Requirements changed.', 'No longer valid: Requirements changed'),
    ('No longer valid: Functionality removed.', 'No longer valid: Functionality removed'),
)

class LockDefectForm(ModelForm, forms.Form):
    reason = forms.ChoiceField(choices = LOCK_REASONS)
        
    class Meta:
        model = Defect
        fields = []