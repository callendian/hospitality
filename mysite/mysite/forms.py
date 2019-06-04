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