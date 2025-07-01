from django.shortcuts import render, get_object_or_404, redirect
import os
from .models import Product

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

    if request.method == 'POST':

        add_to_cart_form = OrderItemForm(request.POST)

        if add_to_cart_form.is_valid():
            print("Form valid:", add_to_cart_form.is_valid(), add_to_cart_form.errors)

            order_item = add_to_cart_form.save(commit=False)
            order_item.product = product
            customer = request.user.customer

            # Obtener o crear una orden activa para el usuario
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            print("Order:", order, "Created:", created)


            # Buscar si ya existe un OrderItem con ese producto en la orden
            existing_item = OrderItem.objects.filter(order=order, product=product).first()

            if existing_item:
                # Sumar cantidades si ya existe ese producto
                existing_item.quantity += order_item.quantity
                existing_item.save()
            else:
                order_item.order = order
                order_item.save()

            return redirect('add_to_cart')  # Redirige a la vista del carrito o a donde prefieras
        else:print('Invalid Form',add_to_cart_form.errors)
    else:
        print('Method is not POST')
        add_to_cart_form = OrderItemForm()

    context = {
        'product': product,
        'form': add_to_cart_form
    }
    return render(request, 'productos/product.html', context)
