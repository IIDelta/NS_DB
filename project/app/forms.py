# forms.py
from django import forms
from .models import DeltekProjectID

class ProjectForm(forms.ModelForm):
    projectid = forms.CharField(required=False, label='Project ID')
    projectname = forms.CharField(required=False, label='Project Name')
    
    class Meta:
        model = DeltekProjectID
        fields = ['projectid', 'projectname']
