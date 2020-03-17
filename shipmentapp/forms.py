from django import forms
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))


class RegistrationForm(forms.Form):
    partner_full_name= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
    }))
    partner_company= forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
    }))
    contact = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
    }))
    alt_contact = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Your alternative contact',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control mb-3',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3',
    }))
    
    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password


class ProfileEditForm(forms.Form):
    partner_full_name = forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',

    }))
    partner_company = forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',

    }))
    contact = forms.IntegerField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Enter your contact',
    }))
    address = forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',

    }))
    alt_contact = forms.IntegerField(required=False,widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Your alternative contact',
    }))
    website = forms.URLField(required=False,widget= forms.URLInput(attrs={
        'class': 'form-control mb-3',

    }))
    description = forms.CharField(required=False,widget= forms.Textarea(attrs={
        'class': 'form-control mb-3',
        'placeholder':"Write about yourself!",

    }))

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data['contact']
        # receiver_alt_contact = cleaned_data['receiver_alt_contact']
        if len(str(contact)) < 10 or len(str(contact)) > 10 :
            raise forms.ValidationError("Your number should be at least 10 Characters")

        return self.cleaned_data


PARCEL_TYPE = (
    ('Clothes', 'Clothes'),
    ('Documents', 'Documents'),
    ('Others', 'Others'),
)

MODE_OF_PAYMENT = (
    ('COD', 'Cash on Delivery'),
    ('Already Paid', 'Already Paid'),
)

class ShipmentForm(forms.Form):
    receiver_name = forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Your Name',
    }))


    receiver_contact = forms.IntegerField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Enter your contact',
    }))

    receiver_alt_contact = forms.IntegerField(required=False,widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Your alternative contact no.',
    }))
    dropoff_city = forms.ChoiceField(widget=forms.Select(attrs={
        "name": "select_0",
        "class": "form-control"}))
    dropoff_street_address = forms.CharField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Street address',
    }))
    receiver_email = forms.EmailField(widget= forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'E-mail',
    }))
    parcel_type = forms.ChoiceField(choices=PARCEL_TYPE,widget=forms.Select(attrs={
        "name": "select_0",
        "class": "form-control"}))
    parcel_weight = forms.DecimalField(widget= forms.NumberInput(attrs={
        'class': 'form-control ',
        'placeholder': '(in gram)',
    }))
    parcel_length = forms.DecimalField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': '(in cm)',
    }))
    parcel_width = forms.DecimalField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': '(in cm)',
    }))
    parcel_height = forms.DecimalField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': '(in cm)',
    }))
    parcel_total = forms.DecimalField(widget= forms.NumberInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'total amount',
    }))
    customer_payment_status = forms.BooleanField(required=False)
    mode_of_payment = forms.ChoiceField(choices=MODE_OF_PAYMENT,widget=forms.Select(attrs={
        "name": "select_0",
        "class": "form-control"}))

    def __init__(self, cities=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dropoff_city'].choices=cities
    
    def clean(self):
        cleaned_data = super().clean()
        receiver_contact = cleaned_data['receiver_contact']
        # receiver_alt_contact = cleaned_data['receiver_alt_contact']
        if len(str(receiver_contact)) < 10:
            raise forms.ValidationError("Your number should be at least 10 Characters")

        return self.cleaned_data


class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'enter old password'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'enter new password'
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'confirm new password'
    }))


    def clean_confirm_new_password(self):
        cleaned_data = super().clean()
        new_password = cleaned_data['new_password']
        confirm_new_password = cleaned_data['confirm_new_password']
        if new_password != confirm_new_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_new_password

    def clean(self):
        cleaned_data = super(PasswordUpdateForm,self).clean()
        new_password = cleaned_data['new_password']

        if len(new_password) < 6:
            raise forms.ValidationError("Your password should be at least 6 Characters")

        return cleaned_data