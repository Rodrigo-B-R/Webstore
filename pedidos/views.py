from django.shortcuts import render
from carrito.models import Order,OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def view_orders(request):
    orders= Order.objects.filter(complete=True, customer= request.user.customer)
    
    order_items_map={}
    shipping_addresses={}
    
    for order in orders:
        order_items= OrderItem.objects.filter(order=order)
        order_items_map[order]=order_items



    context={'orders':orders,'order_items_map':order_items_map,'shipping_addresses':shipping_addresses}

    return render(request,'pedidos/orders.html',context)
