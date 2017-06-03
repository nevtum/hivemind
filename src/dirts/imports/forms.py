from dirts.models import Defect
from django import forms
from django.forms import ModelForm, Textarea
from django.utils import timezone

class ImportDirtsForm(forms.Form):
    project_code = forms.CharField(label='Enter project code to save under')
    import_file = forms.FileField(allow_empty_file=False)