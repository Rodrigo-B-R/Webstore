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
from carrito.models import GuestOrder, GuestOrderItem
from productos.utils import get_or_create_guest_order
from .utils import get_or_create_shipping_address


# Create your views here.


def cart_view_router(request):
    if request.user.is_authenticated:
        return  cart_view_authenticated(request)
    else:
        return cart_view_guest(request)
    

@login_required
def cart_view_authenticated(request):
    customer= request.user.customer
    order, created= Order.objects.get_or_create(customer=customer,complete=False)
    items= order.orderitem_set.all()    
        
        

    context= {'order':order,'items':items}



    return render(request, 'carrito/cart.html', context)

def cart_view_guest(request):
    order_id = request.session.get('guest_order_id')

    if order_id:
        order = get_object_or_404(GuestOrder, id=order_id, complete=False)
    else:
        return redirect('main_page')
    
    order_items= order.items.all()

    context={'order':order, 'items':order_items}

    return render(request, 'carrito/cart.html', context)


def delete_item_router(request, item_id):
    if request.method=='POST':
        if request.user.is_authenticated:
            return  delete_item_view_authenticated(request,item_id)
        else:
            return delete_item_view_guest(request,item_id)
    return redirect('cart')
    
@login_required
def delete_item_view_authenticated(request, item_id):

    order= Order.objects.get(customer=request.user.customer,complete=False)
    item=get_object_or_404(OrderItem,pk=item_id,order=order)
    item.delete()
    return redirect('cart')

def delete_item_view_guest(request,item_id):

    order_id = request.session.get('guest_order_id')

    order = get_object_or_404(GuestOrder, id=order_id, complete=False)
    item= get_object_or_404(GuestOrderItem,id=item_id,order=order)
    item.delete()
    return redirect('cart')
    

def update_quantity_router(request,product_id):
    if request.user.is_authenticated:
        return  update_quantity_authenticated_view(request,product_id)
    else:
        return update_quantity_guest_view(request,product_id)
    

@login_required
def update_quantity_authenticated_view(request,product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        product = get_object_or_404(Product, id=product_id)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
    
def update_quantity_guest_view(request,product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        product = get_object_or_404(Product, id=product_id)
        order_id = request.session.get('guest_order_id')
        order= get_object_or_404(GuestOrder,id=order_id,complete=False)
        order_item= GuestOrderItem.objects.get(order=order,product=product)

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

def checkout_view_router(request,order_id):
    if request.user.is_authenticated:
        return  checkout_view_authenticated(request,order_id)
    else:
        return checkout_view_guest(request)
    

@login_required
def checkout_view_authenticated(request,order_id):

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        customer = request.user.customer
    except customer.DoesNotExist:
    # puedes redirigir a completar perfil o mostrar error
        return redirect('sign_up')

    order= get_object_or_404(Order,pk=order_id,complete=False,customer=request.user.customer)
    
    if check_stock(request,order) == False : return redirect('cart')

    order_items= order.orderitem_set.all()
   
    user=request.user
    shipping_addresses = customer.shippingaddress_set.all()

    
    default_shipping = shipping_addresses.first()  

    if default_shipping:
        shipping_form = ShippingAddressForm(instance=default_shipping)
    else:
        shipping_form = ShippingAddressForm()

    context={'order_items':order_items,'customer':customer, 'user':user,'shipping_addresses':shipping_addresses,'order':order,'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY,'shipping_form':shipping_form}

   
    return render(request,'carrito/checkout.html',context)


def checkout_view_guest(request):
    order_id = request.session.get('guest_order_id')
    order= get_object_or_404(GuestOrder,id=order_id,complete=False)
    
    if check_stock(request,order) == False : return redirect('cart')

    order_items= order.items.all()
   
    context={'order_items':order_items,'order':order,'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY,'shipping_form':ShippingAddressForm,'guest_form':GuestCheckoutForm}

   
    return render(request,'carrito/checkout.html',context)


def process_checkout_router(request,order_id):

    if request.user.is_authenticated:
        return proccess_checkout_view_authenticated(request,order_id)
    else:
        return process_checkout_view_guest(request)

@login_required
def proccess_checkout_view_authenticated(request, order_id):
    order = get_object_or_404(Order, id=order_id, complete=False, customer=request.user.customer)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)

        if form.is_valid():
            shipping_address=get_or_create_shipping_address
            shipping_address = form.save(commit=False)
            shipping_address.customer = request.user.customer
            shipping_address.save()

            # Asociar dirección con la orden
            order.shipping_address = shipping_address
            order.save()

            # Redirigir a la vista que genera la sesión de Stripe
            return redirect('crear_pago',order_id)
        else:
            return render(request, 'carrito/checkout.html', {
                'order': order,
                'order_items': order.orderitem_set.all(),
                'shipping_form': form,
                'shipping_addresses': request.user.customer.shippingaddress_set.all(),
            })

    # Si alguien entra manualmente por GET
    return redirect('cart')  # o podrías mostrar un error


def process_checkout_view_guest(request):
    if request.method == 'POST':
        # Obtenemos la orden del invitado desde la sesión
        order_id = request.session.get('guest_order_id')
        if not order_id:
            return redirect('cart')  # no hay orden = no hay checkout

        order = get_object_or_404(GuestOrder, id=order_id, complete=False)

        # ⚠️ Procesamos los formularios con POST
        shipping_form = ShippingAddressForm(request.POST)
        guest_checkout_form = GuestCheckoutForm(request.POST)

        if guest_checkout_form.is_valid() and shipping_form.is_valid():
            # Guardar dirección de envío
            shipping_address = shipping_form.save(commit=False)
            shipping_address.save()

            # Guardar email del invitado en la orden
            email = guest_checkout_form.cleaned_data['email']
            order.email = email
            order.shipping_address = shipping_address
            order.save()

            # Redirigir a vista de pago (Stripe u otra)
            return redirect('crear_pago', order_id=order.id)
        else:
            return render(request, 'carrito/checkout.html', {
                'order': order,
                'order_items': order.items.all(),
                'shipping_form': shipping_form,
                'guest_checkout_form': guest_checkout_form
            })

    return redirect('cart')