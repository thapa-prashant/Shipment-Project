from django import forms
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(forms.Form):
    partner_full_name= forms.CharField()
    partner_company= forms.CharField()    
    contact = forms.CharField()
    address = forms.CharField()
    username=forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    email=forms.EmailField()
                      
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())   
    
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     User = 
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Username already exists")
    #     return username  
    
    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password  

    
    
       
        
    


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
    receiver_name = forms.CharField()
    receiver_contact = forms.IntegerField()
    receiver_alt_contact = forms.IntegerField(required=False)
    dropoff_city = forms.ChoiceField()
    dropoff_street_address = forms.CharField()
    receiver_email = forms.EmailField()
    parcel_type = forms.ChoiceField(choices=PARCEL_TYPE)
    parcel_weight = forms.DecimalField()
    parcel_length = forms.DecimalField()
    parcel_width = forms.DecimalField()
    parcel_height = forms.DecimalField()
    parcel_total = forms.IntegerField()
    customer_payment_status = forms.BooleanField(required=False)
    mode_of_payment = forms.ChoiceField(choices=MODE_OF_PAYMENT)

    def __init__(self, cities=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dropoff_city'].choices=cities