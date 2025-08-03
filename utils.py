from carrito.models import GuestOrder, GuestOrderItem, Order, OrderItem
from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

def link_guest_orders_to_user(user):
    if not hasattr(user, 'customer'):
        return  

    guest_orders = GuestOrder.objects.filter(email=user.email)
    if not guest_orders.exists():
        return

    customer = user.customer

    # Busca si ya tiene una orden incompleta
    current_order = Order.objects.filter(customer=customer, complete=False).first()

    for guest_order in guest_orders:
        if current_order:
            # fusiona los items en la orden existente
            for item in guest_order.items.all():
                OrderItem.objects.create(
                    order=current_order,
                    product=item.product,
                    quantity=item.quantity
                )
        else:
            # si no había una orden incompleta, crea una nueva
            current_order = Order.objects.create(
                customer=customer,
                date_ordered=guest_order.date_ordered,
                complete=guest_order.complete,
                transaction_id=guest_order.transaction_id,
                shipping_address=guest_order.shipping_address
            )
            for item in guest_order.items.all():
                OrderItem.objects.create(
                    order=current_order,
                    product=item.product,
                    quantity=item.quantity
                )

        guest_order.delete()
