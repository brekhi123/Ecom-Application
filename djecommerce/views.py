from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages  # Import messages module
from core.models import *
from django.shortcuts import render, redirect, get_object_or_404
from customadmin.forms import AddressForm, CouponListForm, ItemForm, OrderItemForm, OrderForm, PaymentForm, RefundForm, PaypalForm


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            # Login the user
            login(request, user)
            # Redirect to admin dashboard or any other desired page
            return redirect('dashboard')
        else:
            # Authentication failed
            messages.warning(request, 'Invalid username or password.')
            return redirect('admin-login')
    
    # For GET request or initial rendering of the login form
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customadmin.forms import AddressForm
from core.models import Address

@login_required
def address_list(request):
    #if request.user.is_superuser:
    addresses = Address.objects.all()
    #else:
    #addresses = Address.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses})

@login_required  # Protect views with login_required decorator
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(user=request.user)  # Pass request.user to form
    return render(request, 'address_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address, user=request.user)  # Pass request.user to form
    return render(request, 'address_edit.html', {'form': form, 'address': address})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'address_delete_confirm.html', {'address': address})


@login_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupon_list.html', {'coupons': coupons})

@login_required  # Protect views with login_required decorator
def add_coupon(request):
    if request.method == 'POST':
        form = CouponListForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponListForm()  # Pass request.user to form
    return render(request, 'coupon_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponListForm(request.POST, instance=coupon)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponListForm(instance=coupon)  # Pass request.user to form
    return render(request, 'coupon_edit.html', {'form': form, 'coupon': coupon})


@login_required
def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('coupon_list')
    return render(request, 'coupon_delete_confirm.html', {'coupon': coupon})


@login_required
def item_list_admin(request):
    itemlist = Item.objects.all()
    return render(request, 'item_list_admin.html', {'itemlist': itemlist})

@login_required  # Protect views with login_required decorator
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('item_list_admin')
    else:
        form = ItemForm()  # Pass request.user to form
    return render(request, 'item_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('item_list_admin')
    else:
        form = ItemForm(instance=item)  # Pass request.user to form
    return render(request, 'item_edit.html', {'form': form, 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list_admin')
    return render(request, 'item_delete_confirm.html', {'item': item})

@login_required
def orderitem_list(request):
    #if request.user.is_superuser:
    orderitemlist = OrderItem.objects.all()
    #else:
       #orderitemlist = OrderItem.objects.filter(user=request.user)
    return render(request, 'orderitem_list.html', {'orderitemlist': orderitemlist})

@login_required  # Protect views with login_required decorator
def add_orderitem(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('orderitem_list')
    else:
        form = OrderItemForm(user=request.user)  # Pass request.user to form
    return render(request, 'orderitem_form.html', {'form': form})



@login_required  # Protect views with login_required decorator
def edit_orderitem(request, pk):
    orderitem = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=orderitem, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('orderitem_list')
    else:
        form = OrderItemForm(instance=orderitem, user=request.user)  # Pass request.user to form
    return render(request, 'orderitem_edit.html', {'form': form, 'orderitem': orderitem})


@login_required
def delete_orderitem(request, pk):
    orderitem = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        orderitem.delete()
        return redirect('orderitem_list')
    return render(request, 'orderitem_delete_confirm.html', {'orderitem': orderitem})


@login_required
def order_list(request):
    #if request.user.is_superuser:
    orderlist = Order.objects.all()
    #else:
    #orderlist = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orderlist': orderlist})

@login_required  # Protect views with login_required decorator
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(user=request.user)  # Pass request.user to form
    return render(request, 'order_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order, user=request.user)  # Pass request.user to form
    return render(request, 'order_edit.html', {'form': form, 'order': order})


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'order_delete_confirm.html', {'order': order})


@login_required
def payment_list(request):
    #if request.user.is_superuser:
    paymentlist = Payment.objects.all()
    #else:
    #orderlist = Order.objects.filter(user=request.user)
    return render(request, 'payment_list.html', {'paymentlist': paymentlist})

@login_required  # Protect views with login_required decorator
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(user=request.user)  # Pass request.user to form
    return render(request, 'payment_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment, user=request.user)  # Pass request.user to form
    return render(request, 'payment_edit.html', {'form': form, 'payment': payment})


@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')
    return render(request, 'payment_delete_confirm.html', {'payment': payment})


@login_required
def refund_list(request):
    #if request.user.is_superuser:
    refundlist = Refund.objects.all()
    #else:
    #orderlist = Order.objects.filter(user=request.user)
    return render(request, 'refund_list.html', {'refundlist': refundlist})

@login_required  # Protect views with login_required decorator
def add_refund(request):
    if request.method == 'POST':
        form = RefundForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('refund_list')
    else:
        form = RefundForm(user=request.user)  # Pass request.user to form
    return render(request, 'refund_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_refund(request, pk):
    refund = get_object_or_404(Refund, pk=pk)
    if request.method == 'POST':
        form = RefundForm(request.POST, instance=refund, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('refund_list')
    else:
        form = RefundForm(instance=refund, user=request.user)  # Pass request.user to form
    return render(request, 'refund_edit.html', {'form': form, 'refund': refund})


@login_required
def delete_refund(request, pk):
    refund = get_object_or_404(Refund, pk=pk)
    if request.method == 'POST':
        refund.delete()
        return redirect('refund_list')
    return render(request, 'refund_delete_confirm.html', {'refund': refund})

@login_required
def paypal_list(request):
    #if request.user.is_superuser:
    paypallist = PayPalTransaction.objects.all()
    #else:
    #orderlist = Order.objects.filter(user=request.user)
    return render(request, 'paypal_list.html', {'paypallist': paypallist})

@login_required  # Protect views with login_required decorator
def add_paypal(request):
    if request.method == 'POST':
        form = PaypalForm(request.POST, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('paypal_list')
    else:
        form = PaypalForm(user=request.user)  # Pass request.user to form
    return render(request, 'paypal_form.html', {'form': form})

@login_required  # Protect views with login_required decorator
def edit_paypal(request, pk):
    payp = get_object_or_404(PayPalTransaction, pk=pk)
    if request.method == 'POST':
        form = PaypalForm(request.POST, instance=payp, user=request.user)  # Pass request.user to form
        if form.is_valid():
            form.save()
            return redirect('paypal_list')
    else:
        form = PaypalForm(instance=payp, user=request.user)  # Pass request.user to form
    return render(request, 'paypal_edit.html', {'form': form, 'payp': payp})


@login_required
def delete_paypal(request, pk):
    payp = get_object_or_404(PayPalTransaction, pk=pk)
    if request.method == 'POST':
        payp.delete()
        return redirect('paypal_list')
    return render(request, 'paypal_delete_confirm.html', {'payp': payp})