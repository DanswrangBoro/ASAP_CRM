from django import forms

from django import forms
from .models import Center,CustomUser
class UserCreationForm(forms.ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phoneNumber', 'role', 'password', 'blocked', 'center']
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Override the save method to handle center assignment
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()  # Required for saving ManyToMany fields
        return user

    def clean_confirmPassword(self):
        password = self.cleaned_data.get("password")
        confirmPassword = self.cleaned_data.get("confirmPassword")
        if password and confirmPassword and password != confirmPassword:
            raise forms.ValidationError("Passwords do not match")
        return confirmPassword

    # Override the __init__ method to dynamically set the queryset for the center field
    def __init__(self, *args, **kwargs):
        center_queryset = kwargs.pop('center_queryset', None)
        super().__init__(*args, **kwargs)
        if center_queryset is not None:
            self.fields['center'].queryset = center_queryset
