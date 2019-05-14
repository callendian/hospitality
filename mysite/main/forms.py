from django import forms
from .models import *


class TourSearchForm(forms.ModelForm):
    tourType = forms.ModelChoiceField(
        queryset=TourType.objects.all().values_list('name', flat=True), 
        label='Tour Type', widget=forms.Select())
    city = forms.ModelChoiceField(
        queryset=City.objects.all().values_list('name', flat=True), 
        label='City', widget=forms.Select())
    min_days = forms.IntegerField(min_value=1, label='Min Duration (days)')
    max_days = forms.IntegerField(min_value=1, label='Max Duration (days)')

    class Meta:
        model = Tour
        exclude = ['guide', 'description', 'price', 'days']
