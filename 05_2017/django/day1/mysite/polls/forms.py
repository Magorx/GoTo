from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
