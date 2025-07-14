from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import OrderItem, Order
from .forms import OrderItemForm
from productos.models import Product, ProductImage
from django.conf import settings
from .utils import verificar_stock
from usuarios.forms import ShippingAddressForm


# Create your views here.
@login_required
def proccess_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, complete=False, customer=request.user.customer)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)

        if form.is_valid():
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



# @login_required
def cart_view(request):

    if request.user.is_authenticated:

        customer= request.user.customer
    
        order, created= Order.objects.get_or_create(customer=customer,complete=False)

        items= order.orderitem_set.all()    
        
        

        context= {'order':order,'items':items}



        return render(request, 'carrito/cart.html', context)



def delete_item_view(request, item_id):

    if request.method=='POST':
        order= Order.objects.get(customer=request.user.customer,complete=False)
        item=get_object_or_404(OrderItem,pk=item_id,order=order)
        item.delete()
        return redirect('cart')
            


@login_required
def update_quantity_view(request, product_id):
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
    


def checkout_view(request,order_id):

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        customer = request.user.customer
    except customer.DoesNotExist:
    # puedes redirigir a completar perfil o mostrar error
        return redirect('sign_up')

    order= get_object_or_404(Order,pk=order_id,complete=False,customer=request.user.customer)
    
    if verificar_stock(order) == False : return redirect('cart')

    order_items= order.orderitem_set.all()
   
    user=request.user
    shipping_addresses = customer.shippingaddress_set.all()

    context={'order_items':order_items,'customer':customer, 'user':user,'shipping_addresses':shipping_addresses,'order':order,'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY,'shipping_form':ShippingAddressForm}

   
    return render(request,'carrito/checkout.html',context)
    

