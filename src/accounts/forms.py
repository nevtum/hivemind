from django import forms
from .models import SignupRequest
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = SignupRequest
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
    
    # def save(self):
    #     username = self.cleaned_data["username"]
    #     exists = User.objects.get(username=username)
    #     if exists:
    #         raise forms.ValidationError(
    #             u'User %s already exists!' % username
    #         )