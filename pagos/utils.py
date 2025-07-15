from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from carrito.models import GuestOrder,Order
from django.utils import timezone
from django.http import Http404


def check_shipping_addres(order):
    if not order.shipping_address:
        return redirect('process_checkout', order_id=order.id)
    return

#2
def get_order(request, order_id=None, is_complete=False):
    filters = {'complete': is_complete}

    if request.user.is_authenticated:
        filters['customer'] = request.user.customer
        if order_id:
            filters['id'] = order_id
        if is_complete:
            return get_object_or_404(Order, **filters)
        # Autocreación si no existe (carrito)
        order, _ = Order.objects.get_or_create(**filters)
        return order
    else:
        # Orden de invitado
        if order_id:
            filters['id'] = order_id
        else:
            order_id = request.session.get('guest_order_id')
            if not order_id:
                if is_complete:
                    raise Http404("No guest order found.")
                # Crear nueva orden de invitado
                order = GuestOrder.objects.create()
                request.session['guest_order_id'] = order.id
                return order
            filters['id'] = order_id

        return get_object_or_404(GuestOrder, **filters)
        
       
#5
def get_order_by_id(order_id,is_complete=False):

    try:
        return Order.objects.get(id=order_id, complete=is_complete)
    except Order.DoesNotExist:
        return get_object_or_404(GuestOrder, id=order_id, complete=is_complete)
    

def update_order(order):
    for item in order.items.all():
        product = item.product
        product.stock -= item.quantity
        product.save()

    order.complete = True
    order.date_ordered= timezone.now()
    order.save()   