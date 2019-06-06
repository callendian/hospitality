from django import forms

STAR_RATING = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)

class DisputeForm(forms.Form):
    bookingID = forms.IntegerField(label="Booking ID", required=True)
    description = forms.CharField(label='Description', max_length=250, required=True)

class DisputeID(forms.Form):
    bookingID = forms.IntegerField(label="Booking ID", required=True)

class VisitorReviewForm(forms.Form):
    bookingID = forms.IntegerField(label="Booking ID", required=True)
    description = forms.CharField(label='Description', max_length=250, required=True)
    rating = forms.ChoiceField(choices=STAR_RATING, required=True)

class contactUSForm(forms.Form):
    name = forms.CharField(label='Name', max_length=250, required=True)
    email = forms.CharField(label='Email', max_length=30, required=True)
    description = forms.CharField(label='Description', max_length=500, required=True)
