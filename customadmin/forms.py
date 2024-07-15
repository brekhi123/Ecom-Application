from django import forms
from core.models import Address, Coupon, Item, OrderItem, Order, Payment, Refund, PayPalTransaction

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_address', 'country', 'zip', 'address_type', 'default']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddressForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddressForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance



class CouponListForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CouponListForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CouponListForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'discount_price', 
                  'category', 'label', 'slug', 
                  'description', 'small_description', 'image', 'is_trending']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ItemForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ItemForm, self).save(commit=False)
        instance.user = self.user  
        if commit:
            instance.save()
        return instance
    

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['user', 'ordered', 'item', 'quantity']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderItemForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(OrderItemForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'ref_code', 'items', 'ordered_date', 'ordered',
                  'shipping_address', 'billing_address', 'payment',
                  'coupon', 'being_delivered', 'received',
                  'refund_requested', 'refund_granted']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(OrderForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['stripe_charge_id', 'user', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PaymentForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance
    

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['order', 'reason', 'accepted', 'email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RefundForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(RefundForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance
    
class PaypalForm(forms.ModelForm):
    class Meta:
        model = PayPalTransaction
        fields = ['user', 'transaction_id', 'amount', 'status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PaypalForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(PaypalForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the address
        if commit:
            instance.save()
        return instance