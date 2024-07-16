# forms.py
from django import forms
from .models import DeltekProjectID

class ProjectForm(forms.ModelForm):
    projectid = forms.CharField(required=False, label='Project ID')
    projectname = forms.CharField(required=False, label='Project Name')
    sponsorname = forms.CharField(required=False, label='Sponsor Name')
    
    class Meta:
        model = DeltekProjectID
        fields = ['projectid', 'projectname', 'sponsorname']
