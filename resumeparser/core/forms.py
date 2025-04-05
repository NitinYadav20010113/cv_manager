from django import forms
from .models import Details
from django.core import validators

class Emp(forms.ModelForm):
    class Meta:
        model = Details
        fields = '__all__'
