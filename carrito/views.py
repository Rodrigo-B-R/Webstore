from django.shortcuts import render, get_object_or_404, redirect

from .models import OrderItem, Order
from .forms import OrderItemForm
from productos.models import Product

# Create your views here.


def cart_view(request,id):

    product = get_object_or_404(Product, id=id)

    if request.method=='POST':
        form= OrderItemForm(request.POST)

        if form.is_valid():
            order_item= form.save(commit=False)
            order_item.product= product 
            customer= request.user.customer
            customer = request.user.customer

            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            order_item.order = order
            order_item.save()

            return redirect('cart')
    else:
        form= OrderItemForm()

    context = {'form': form, 'product': product}


    return render(request,'carrito/add_to_cart.html',context)

