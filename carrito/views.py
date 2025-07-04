from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


from .models import OrderItem, Order
from .forms import OrderItemForm
from productos.models import Product, ProductImage

# Create your views here.




@login_required
def cart_view(request):
    customer= request.user.customer

    try:
        order= Order.objects.get(customer=customer)
    
    except Order.DoesNotExist : 
        order = Order.objects.create(customer=request.user.customer, complete=False)

    items= OrderItem.objects.filter(order=order)
    

    context= {'order':order,'items':items}



    return render(request, 'carrito/cart.html', context)
