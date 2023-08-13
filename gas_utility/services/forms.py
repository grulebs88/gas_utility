from django import forms
from .models import ServiceRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'details', 'attachment']

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        details = cleaned_data.get('details')
        attachment = cleaned_data.get('attachment')

        # Add your validation logic here
        if not service_type:
            raise forms.ValidationError('Please select a service type.')
        if not details:
            raise forms.ValidationError('Please provide details about your service request.')

class ServiceRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']