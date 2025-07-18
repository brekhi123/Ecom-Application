from django.urls import path
from.views import ItemDetailView, CheckoutView, HomeView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, PaymentView, AddCouponView, RequestRefundView, PayPal, paypal_return, paypal_cancel

app_name = 'core'
urlpatterns =  [
    path('', HomeView.as_view(), name='home-page'),
    path('checkout/', CheckoutView.as_view(), name='checkout-page'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>', ItemDetailView.as_view(), name='product-page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('paypal/', PayPal, name='paypal'),
    path('paypal-return/', paypal_return, name='paypal-return'),
    path('paypal-cancel/', paypal_cancel, name='paypal-cancel'),
]