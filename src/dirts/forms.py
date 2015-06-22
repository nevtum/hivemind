from django import forms

class CreateDirtForm(forms.Form):
    project_code = forms.CharField(max_length=20)
    release_id = forms.CharField(max_length=50)
    reference = forms.CharField(max_length=1000)
    # status = ...
    title = forms.CharField(max_length=80)
    description = forms.CharField(max_length=2000, widget=forms.Textarea)
