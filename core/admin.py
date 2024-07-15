from django.contrib import admin
from .models import Item, Order, OrderItem, Payment, Coupon, Refund, Address
#from .models import Coupon


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
    make_refund_accepted.short_descritpion = 'Update orders to refund granted'

def make_order_received(modeladmin, request, queryset):
    queryset.update(being_delivered=False, received=True)
    make_order_received.short_descritpion = 'Update orders to be received'
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 
                    'ordered', 
                    'being_delivered',
                    'received', 
                    'refund_requested', 
                    'refund_granted', 
                    'billing_address',
                    'shipping_address',
                    'payment',
                    'coupon'
                    ]

    list_display_links = [
        'user',
        'billing_address',
        'shipping_address',
        'payment',
        'coupon'
    ]

    list_filter = ['user', 
                   'ordered', 
                   'being_delivered', 
                   'received', 
                   'refund_requested', 
                   'refund_granted'
                   ]

    search_fields = [
        'user__username', 'ref_code'
    ]

    actions = [
        make_refund_accepted, make_order_received
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address', 
        'apartment_address', 
        'country', 
        'zip',
        'address_type',
        'default'
    ]

    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 
                     'street_address', 
                     'apartment_address', 
                     'zip'
                     ]


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'small_description', 'price', 'is_trending']  # Add 'is_trending' to display in the admin list
    list_filter = ['is_trending']  # Add filter option for 'is_trending'


class OrderItemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is superuser, return all order items
        if request.user.is_superuser:
            return qs
        # Otherwise, return order items only for the current user
        return qs.filter(user=request.user)

# admin.py

from django.contrib import admin
from .models import PayPalTransaction

@admin.register(PayPalTransaction)
class PayPalTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('user__username', 'transaction_id')



admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)


