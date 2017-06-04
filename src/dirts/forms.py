from django import forms
from django.forms import ModelForm, Textarea
from django.utils import timezone

from .models import Defect


class ViewDirtReportForm(ModelForm, forms.Form):
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

class ReopenDirtForm(ModelForm, forms.Form):
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Defect
        fields = [
            'release_id',
        ]

class CloseDirtForm(ModelForm, forms.Form):
    class Meta:
        model = Defect
        fields = [
            'release_id',
        ]
        
    reason = forms.CharField(widget=forms.Textarea, required=False)
