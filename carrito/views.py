from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import OrderItem, Order
from .forms import OrderItemForm, GuestCheckoutForm
from productos.models import Product, ProductImage
from django.conf import settings
from .utils import check_stock
from usuarios.forms import ShippingAddressForm
# from carrito.models import GuestOrder, GuestOrderItem
# from productos.utils import get_or_create_guest_order
from .utils import get_or_create_shipping_address, get_item
from pagos.utils import get_order
from django.http import Http404

# Create your views here.

def delete_item_view(request,item_id):
    order=get_order(request)
    item=get_item(request,item_id,order,by='item')
    item.delete()
    return redirect('cart')

def update_quantity_view(request,product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        product = get_object_or_404(Product, id=product_id)
        
        order= get_order(request)
        order_item= get_item(request,product_id,order)
        
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
    

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def checkout_view(request, order_id):
    try:
        order = get_order(request, order_id)
    except:
        return redirect('cart')

    if not check_stock(request, order):
        return redirect('cart')

    order_items = order.items.all()
    context = {
        'order_items': order_items,
        'order': order,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    if request.user.is_authenticated:
        customer = request.user.customer
        shipping_addresses = customer.shippingaddress_set.all()
        default_shipping = shipping_addresses.first()

        shipping_form = ShippingAddressForm(instance=default_shipping) if default_shipping else ShippingAddressForm()

        context.update({
            'customer': customer,
            'user': request.user,
            'shipping_addresses': shipping_addresses,
            'shipping_form': shipping_form,
        })

    else:
        context.update({
            'shipping_form': ShippingAddressForm(),
            'guest_form': GuestCheckoutForm(),
        })

    return render(request, 'carrito/checkout.html', context)


def process_checkout_view(request, order_id):
    order = get_order(request, order_id)

    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST)
        guest_checkout_form = GuestCheckoutForm(request.POST) if not request.user.is_authenticated else None

        if shipping_form.is_valid() and (request.user.is_authenticated or guest_checkout_form.is_valid()):
            shipping_address = shipping_form.save(commit=False)

            # Solo asignamos customer si está autenticado
            if request.user.is_authenticated:
                shipping_address.customer = request.user.customer

            shipping_address.save()

            # Asociar dirección con la orden
            order.shipping_address = shipping_address

            # Si es invitado, guardar su email
            if not request.user.is_authenticated:
                order.email = guest_checkout_form.cleaned_data['email']

            order.save()

            return redirect('crear_pago', order_id)

        # Si los formularios no son válidos
        context = {
            'order': order,
            'order_items': order.items.all(),
            'shipping_form': shipping_form,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        }

        if request.user.is_authenticated:
            context['shipping_addresses'] = request.user.customer.shippingaddress_set.all()
        else:
            context['guest_checkout_form'] = guest_checkout_form

        return render(request, 'carrito/checkout.html', context)

    return redirect('cart')

def cart_view(request):
    try:
        order = get_order(request, is_complete=False)
    except Http404:
        return redirect('main_page')  # o puedes mostrar una página de carrito vacío

    context = {
        'order': order,
        'items': order.items.all()
    }

    return render(request, 'carrito/cart.html', context)