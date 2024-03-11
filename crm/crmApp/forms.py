from django import forms

class UserCreationForm(forms.Form):
    userName = forms.CharField(max_length=100)
    email = forms.EmailField()
    phoneNumber = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=[('manager', 'Manager'), ('agent', 'Agent')])
    team = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmPassword = forms.CharField(widget=forms.PasswordInput)