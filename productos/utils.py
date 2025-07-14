from .models import Product
from carrito.models import GuestOrder, GuestOrderItem
from django.shortcuts import render, redirect, get_object_or_404

def get_or_create_guest_order(request):
    order_id = request.session.get('guest_order_id')
    order = None
    if order_id:
        try:
            order = GuestOrder.objects.get(id=order_id, complete=False)
        except GuestOrder.DoesNotExist:
            request.session.pop('guest_order_id', None) # no pasa nada, crearemos una nueva abajo
    if not order:
        order = GuestOrder.objects.create()
        request.session['guest_order_id'] = order.id
    return order

def get_product_or_redirect(product_id):
    try:
        product = Product.objects.get(id=product_id, visible=True)
        if product.stock < 1:
            product.visible = False
            product.save()
            return None
        return product
    except Product.DoesNotExist:
        return None
