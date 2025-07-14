from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from carrito.models import Order, OrderItem
from usuarios.models import ShippingAddress
from productos.models import Product
from .utils import verificar_stock
from .forms import GuestCheckoutForm
from django.conf import settings
import json
from django.utils import timezone
from .models import GuestOrder
from usuarios.forms import ShippingAddressForm


def get_or_create_order(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order_id = request.session.get('guest_order_id')
        if order_id:
            order = get_object_or_404(GuestOrder, id=order_id, complete=False)
        else:
            order = GuestOrder.objects.create()
            request.session['guest_order_id'] = order.id
    return order


def cart_view(request):
    order = get_or_create_order(request)
    items = order.orderitem_set.all() if hasattr(order, 'orderitem_set') else []
    return render(request, 'carrito/cart.html', {'order': order, 'items': items})


def delete_item_view(request, item_id):
    if request.method == 'POST':
        order = get_or_create_order(request)
        item = get_object_or_404(OrderItem, pk=item_id, order=order)
        item.delete()
        return redirect('cart')


def update_quantity_view(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        product = get_object_or_404(Product, id=product_id)
        order = get_or_create_order(request)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'increase' and order_item.quantity < product.stock:
            order_item.quantity += 1
        elif action == 'decrease':
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order_item.delete()
                return JsonResponse({'status': 'deleted'})

        order_item.save()
        return JsonResponse({'status': 'ok', 'quantity': order_item.quantity})


def checkout_view(request):
    order = get_or_create_order(request)

    if hasattr(order, 'customer') and not verificar_stock(order):
        return redirect('cart')

    if not hasattr(order, 'customer') and not order.orderitem_set.exists():
        return redirect('cart')

    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST)
        guest_form = GuestCheckoutForm(request.POST) if not request.user.is_authenticated else None

        if shipping_form.is_valid() and (request.user.is_authenticated or guest_form.is_valid()):
            shipping = shipping_form.save()

            if request.user.is_authenticated:
                shipping.customer = request.user.customer
                shipping.save()
                order.shipping_address = shipping
                order.save()
                return redirect('crear_pago', order.id)
            else:
                order.email = guest_form.cleaned_data['email']
                order.shipping_address = shipping
                order.save()
                return redirect('crear_pago_invitado', order.id)
    else:
        shipping_form = ShippingAddressForm()
        guest_form = GuestCheckoutForm() if not request.user.is_authenticated else None

    order_items = order.orderitem_set.all()
    shipping_addresses = order.customer.shippingaddress_set.all() if request.user.is_authenticated else None

    context = {
        'order': order,
        'order_items': order_items,
        'shipping_form': shipping_form,
        'guest_form': guest_form,
        'shipping_addresses': shipping_addresses,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'carrito/checkout.html', context)


def proccess_checkout(request, order_id):
    return redirect('checkout')
