from django import forms
from .models import *


class TourCreationForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=50)
    tourType = forms.ModelChoiceField(
        queryset=TourType.objects.all().values_list('name', flat=True),
        label='Tour Type', widget=forms.Select())
    city = forms.ModelChoiceField(
        queryset=City.objects.all().values_list('name', flat=True),
        label='City', widget=forms.Select())
    description = forms.CharField(
        label='Description', widget=forms.TextInput(attrs={'size': '50'}))
    days = forms.IntegerField(min_value=1, label='Duration (days)')
    price = forms.DecimalField(min_value=0, label='Price (USD)', decimal_places=2)
    
    class Meta:
        model = Tour
        exclude = ['guide']


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


class TourRequestForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = TourRequest
        exclude = ['tour', 'visitor', 'last_modified']

    def clean(self):
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            msg = u"End date should be greater than start date."
            self._errors["end_date"] = self.error_class([msg])
