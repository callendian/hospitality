from django import forms

class DisputeForm(forms.Form):
    bookingID = forms.IntegerField(label="Booking ID", required=True)
    description = forms.CharField(label='Description', max_length=250, required=True)
