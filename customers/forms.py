from django import forms
from .models import Customer

class CreateCustomersForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('fullName', 'email', 'password', 'phoneNumber')

class SigninCustomersForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('email', 'password',)