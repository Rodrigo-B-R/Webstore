from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
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


def delete_item_view(request, id):

    if request.method=='POST':
        order= Order.objects.get(customer=request.user.customer,complete=False )
        item=get_object_or_404(OrderItem,pk=id,order=order)
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

    order= get_object_or_404(Order,pk=order_id,complete=False)
    order_items= order.orderitem_set.all()

    products=[]

    for order_item in order_items:
        if order_item.product.stock >= order_item.quantity:
            
            
            continue
        else:
            return redirect('cart')
    
   
    user=request.user
    shipping_addresses = customer.shippingaddress_set.all()


    
    

    context={'order_items':order_items,'customer':customer, 'user':user,'shipping_addresses':shipping_addresses,'order':order}


        
    return render(request,'carrito/checkout.html',context)
    
