from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label="(Select a Country)").formfield(required=False,
    widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id': 'zip'
    }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label="(Select a Country)").formfield(required=False,
    widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id': 'zip'
    }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing= forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)



class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria-label': 'Recipient\\s username',
        'aria-describedby': 'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()






class PaymentForm(forms.Form):
    stripeToken = forms.CharField(max_length=500, required=True, widget=forms.HiddenInput())
    save_card_info = forms.BooleanField(label='Save card information for future use', required=False)
    card_last_4 = forms.CharField(max_length=4, required=False, widget=forms.HiddenInput(attrs={'id': 'card-last-4'}))
    card_expiry = forms.CharField(max_length=5, required=False, widget=forms.HiddenInput(attrs={'id': 'card-expiry'}))
