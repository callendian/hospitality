from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password',
        max_length=30, required=True)
    passwordconf = forms.CharField(widget=forms.PasswordInput, label='Password Confirmation',
        max_length=30, required=True)
    email = forms.CharField(label='Email', max_length=30, required=True)
    first_name = forms.CharField(label='First Name', max_length=30, required=True)
    last_name = forms.CharField(label='Last Name', max_length=30, required=True)

class SigninForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', 
        max_length=30, required=True)
