from django.shortcuts import render, get_object_or_404, redirect
import os
from .models import Product
from django.utils import timezone


#Importo los modelos y forms de carrito
from carrito.forms import OrderItemForm
from carrito.models import Order, OrderItem

from django.contrib.auth.decorators import login_required

# Create your views here.


def main_page_view(request):

    products= Product.objects.all()

    context={'products':products}




    return render(request,'productos/main_page.html',context=context)


@login_required
def product_view(request,id):
    #usa la logica de carrito para añadir productos 
    product = get_object_or_404(Product, id=id)
    product_quantity= product.stock

    add_to_cart_form = OrderItemForm()

    if request.method == 'POST':

        add_to_cart_form = OrderItemForm(request.POST)

        if add_to_cart_form.is_valid():

            order_item = add_to_cart_form.save(commit=False)
            order_item.product = product
            customer = request.user.customer

            # Obtener o crear una orden activa para el usuario
            order, created = Order.objects.get_or_create(customer=customer, complete=False)


            # Buscar si ya existe un OrderItem con ese producto en la orden
            existing_item = OrderItem.objects.filter(order=order, product=product).first()

            if existing_item:
                # Sumar cantidades si ya existe ese producto
                existing_item.quantity += order_item.quantity

                if existing_item.quantity <= product_quantity:
                    existing_item.save()
                    return redirect('add_to_cart')
                else: 
                    context = {
                                'product': product,
                                'form': add_to_cart_form,
                                'message': 'Product out of stock'
                                }
                    return render(request, 'productos/product.html',context)
            else:
                if order_item.quantity <= product_quantity:
                    order_item.order = order
                    order_item.save()
                    return redirect('add_to_cart')
                else:
                    message = 'Product out of stock'

                    # si no se pudo guardar por stock insuficiente
                    context = {
                        'product': product,
                        'form': add_to_cart_form,
                        'message': message
                    }

        
    context = {
        'product': product,
        'form': add_to_cart_form
    }
    return render(request, 'productos/product.html', context)
