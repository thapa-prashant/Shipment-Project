from django import forms
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User


class WareHouseAdminLoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))


class ShipmentLocationForm(forms.Form):
    shipment = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'sshipment_id'
    }))
    warehouse = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'swarehouse_id'
    }))
    status = forms.CharField(widget = forms.TextInput())
    note = forms.CharField(widget = forms.TextInput())