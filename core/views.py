from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from.models import Item, OrderItem, Order, Address, Payment, Coupon, Refund
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
import stripe
import random
import string
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.db.models import Q
from django.db import transaction





#stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

'''
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")
        '''


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        
        if query:
            queryset = Item.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        elif category:
            queryset = Item.objects.filter(category=category)
        else:
            queryset = Item.objects.all()
        
        return queryset

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")





class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        # Check if the item is in the cart
        object_in_cart = self.object_in_cart(item)
        context['object_in_cart'] = object_in_cart
        # Manually select the trending products based on the 'is_trending' field
        trending_products = Item.objects.filter(is_trending=True)[:3]
        context['trending_products'] = trending_products
        return context

    def object_in_cart(self, item):
        # Check if the item is in the current user's cart
        if self.request.user.is_authenticated:
            user = self.request.user
            order_qs = Order.objects.filter(user=user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                return order.items.filter(item=item).exists()
        return False




class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(self.request, 'checkout-page.html', context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout-page")
        
        '''
        
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # Handling shipping address
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Default Shipping")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.warning(self.request, "No default shipping address available.")
                        return redirect('core:checkout-page')
                else:
                    print('User is entering a new shipping address')
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.warning(self.request, 'Please fill in the shipping address fields.')
                        return redirect('core:checkout-page')

                # Handling billing address
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Default Billing")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.warning(self.request, "No default billing address available.")
                        return redirect('core:checkout-page')
                else:
                    print('User is entering a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):

                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.warning(self.request, 'Please fill in the billing address fields.')
                        return redirect('core:checkout-page')

                # Redirect to payment option
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:paypal')
                else:
                    messages.warning(self.request, "Invalid Payment Option Detected")
                    return redirect('core:checkout-page')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("core:order-summary")
      
'''

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # Handling shipping address
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Default Shipping")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.warning(self.request, "No default shipping address available.")
                        return redirect('core:checkout-page')
                else:
                    print('User is entering a new shipping address')
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            # Set new address as default and update existing default address if any
                            Address.objects.filter(
                                user=self.request.user,
                                address_type='S',
                                default=True
                            ).update(default=False)
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.warning(self.request, 'Please fill in the shipping address fields.')
                        return redirect('core:checkout-page')

                # Handling billing address
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Default Billing")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.warning(self.request, "No default billing address available.")
                        return redirect('core:checkout-page')
                else:
                    print('User is entering a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):

                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            # Set new address as default and update existing default address if any
                            Address.objects.filter(
                                user=self.request.user,
                                address_type='B',
                                default=True
                            ).update(default=False)
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.warning(self.request, 'Please fill in the billing address fields.')
                        return redirect('core:checkout-page')

                # Redirect to payment option
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:paypal')
                else:
                    messages.warning(self.request, "Invalid Payment Option Detected")
                    return redirect('core:checkout-page')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("core:order-summary")

            

def product_view(request, slug):
    return render(request, 'product-page.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # Set the quantity to 1 when the item is removed
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)

    
        
        

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the order does not contain the item
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product-page", slug=slug)
    else:
        # add a message saying the user does not have an order
        messages.info(request, "You do not have an active order.")
        return redirect("core:product-page", slug=slug)
    

class PaymentView(View):
    def get(self, *args, **kwargs):
        # Display the payment page
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
            'order': order,
            'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address.")
            return redirect("core:checkout-page")

    
    def post(self, *args, **kwargs):
        try:
            self.process_payment()
            messages.success(self.request, "Your order was successful!")
        except stripe.error.StripeError as e:
            self.handle_stripe_error(e)
        except Exception as e:
            self.handle_generic_error()
        return redirect("/")

    def process_payment(self):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('payment_method_id')
        amount = int(order.get_total() * 100)
        payment_method_id = self.request.POST.get('payment_method_id')
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create a PaymentIntent using Stripe API
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method=payment_method_id,
            confirmation_method="manual",
            confirm=True,
            return_url=self.request.build_absolute_uri('/')  # Set return URL to home page
        )

        # Create Payment instance
        payment = Payment()
        payment.stripe_charge_id = intent.id
        payment.user = self.request.user
        payment.amount = order.get_total()
        payment.save()

        # Assign the payment to the order
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        #Assign ref_code
        order.ref_code = create_ref_code()
        order.save()

    def handle_stripe_error(self, e):
        error_messages = {
            stripe.error.CardError: f"{e.user_message}",
            stripe.error.RateLimitError: "Too many requests made to the API too quickly. Please try again later.",
            stripe.error.InvalidRequestError: "Invalid parameters were supplied to Stripe's API.",
            stripe.error.AuthenticationError: "Authentication with Stripe's API failed. Please check your API keys.",
            stripe.error.APIConnectionError: "Network communication with Stripe failed. Please check your internet connection."
        }
        messages.warning(self.request, error_messages.get(type(e), "Something went wrong with the payment. You were not charged. Please try again."))

    def handle_generic_error(self):
        messages.warning(self.request, "An unexpected error occurred. Please try again later.")


def get_coupon(request, code):
    coupon = Coupon.objects.get(code=code)
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon

    except ObjectDoesNotExist:
        messages.info(request, "This coupon is invalid.")
        return redirect("core:checkout-page")

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'The coupon has been successfully applied!')
                return redirect('core:checkout-page')

            except ObjectDoesNotExist:
                messages.info(self.request, "This coupon does not exist.")
                return redirect("core:checkout-page")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request,"request_refund.html", context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            #edit order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                #store refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid

from .models import Order, Address, Payment

# views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from paypal.standard.forms import PayPalPaymentsForm
from .models import PayPalTransaction
from .models import Order
import uuid
from paypal.standard.ipn.models import PayPalIPN


def PayPal(request):
    # Get the latest order for the current authenticated user
    order = Order.objects.filter(user=request.user, ordered=False).latest('start_date')
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.get_total(),
        'item_name': 'Order {}'.format(order.pk),
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',  # Ensure this matches your IPN URL config
        'return_url': f'http://{host}{reverse("core:paypal-return")}',
        'cancel_return': f'http://{host}{reverse("core:paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'paypal.html', context)

@csrf_exempt
def paypal_ipn(request):
    # Handle PayPal IPN
    ipn_obj = None
    try:
        ipn_obj = PayPalIPN(request.POST)
        ipn_obj.verify()  # Verify the IPN
    except Exception as e:
        # Log or handle exceptions as needed
        return HttpResponse(status=500)

    if ipn_obj.payment_status == "Completed":
        # Payment was successful, save transaction details to database
        transaction = PayPalTransaction.objects.create(
            user=request.user,
            transaction_id=ipn_obj.txn_id,
            amount=ipn_obj.mc_gross,
            status=ipn_obj.payment_status
        )
        # Additional processing or notifications can be added here

    return HttpResponse(status=200)

def paypal_return(request):
    messages.success(request, "Your order was successful!")
    return redirect('core:home-page')

def paypal_cancel(request):
    messages.warning(request, "Your order has been cancelled.")
    return redirect('core:home-page')


