from django.shortcuts import render, get_object_or_404, redirect
import os
from .models import Product

#Importo los modelos y forms de carrito
from carrito.forms import OrderItemForm, GuestOrderItemForm
from carrito.models import Order, OrderItem, GuestOrder, GuestOrderItem

from django.contrib.auth.decorators import login_required
from .utils import get_product_or_redirect

# Create your views here.


def main_page_view(request):

    products= Product.objects.filter(visible=True)

    context={'products':products}




    return render(request,'productos/main_page.html',context=context)

def product_router_view(request, product_id):
    if request.user.is_authenticated:
        return product_view_authenticated(request, product_id)
    else:
        return product_view_guest(request, product_id)



@login_required
def product_view_authenticated(request, product_id):
    product = get_product_or_redirect(product_id)
    if not product:
        return redirect('main_page')

    form = OrderItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order_item = form.save(commit=False)
        order_item.product = product
        order, _ = Order.objects.get_or_create(customer=request.user.customer, complete=False)

        existing_item = OrderItem.objects.filter(order=order, product=product).first()

        if existing_item:
            existing_item.quantity += order_item.quantity
            if existing_item.quantity <= product.stock:
                existing_item.save()
                return redirect('cart')
        else:
            if order_item.quantity <= product.stock:
                order_item.order = order
                order_item.save()
                return redirect('cart')

        return render(request, 'productos/product.html', {
            'product': product,
            'form': form,
            'message': 'Product out of stock',
        })

    return render(request, 'productos/product.html', {'product': product, 'form': form})



def product_view_guest(request, product_id):
    product = get_product_or_redirect(product_id)
    if not product:
        return redirect('main_page')

    form = GuestOrderItemForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order_item = form.save(commit=False)
        order_item.product = product

        order_id = request.session.get('guest_order_id')
        if order_id:
            order = get_object_or_404(GuestOrder, id=order_id, complete=False)
        else:
            order = GuestOrder.objects.create()
            request.session['guest_order_id'] = order.id

        existing_item = GuestOrderItem.objects.filter(order=order, product=product).first()

        if existing_item:
            existing_item.quantity += order_item.quantity
            if existing_item.quantity <= product.stock:
                existing_item.save()
                return redirect('cart')
        else:
            if order_item.quantity <= product.stock:
                order_item.order = order
                order_item.save()
                return redirect('cart')

        return render(request, 'productos/product.html', {
            'product': product,
            'form': form,
            'message': 'Product out of stock',
        })

    return render(request, 'productos/product.html', {'product': product, 'form': form})




