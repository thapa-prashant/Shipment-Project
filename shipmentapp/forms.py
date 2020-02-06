from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


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