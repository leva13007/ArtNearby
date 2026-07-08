from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomRegistrationForm(forms.Form):
    # Common fields
    username = forms.CharField(label="Username", max_length=150)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # Individual fields
    birthdate = forms.DateField(label="Birthdate", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    # Company fields
    company_name = forms.CharField(label="Company Name", required=False)
    address = forms.CharField(label="Address", required=False)
    phone = forms.CharField(label="Phone", required=False)
    tax_id = forms.CharField(label="Tax ID", required=False)

    # Add a field to distinguish between individual and company
    user_type = forms.ChoiceField(
        label="User Type",
        choices=[('individual', 'Individual'), ('company', 'Company')],
        widget=forms.RadioSelect,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data