from carrito.models import GuestOrder, GuestOrderItem, Order, OrderItem
from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
def link_guest_orders_to_user(user):

    if not hasattr(user, 'customer'):
        return  

    customer = user.customer
    guest_orders = GuestOrder.objects.filter(email=user.email)

    for guest_order in guest_orders:
        new_order= Order.objects.create(
            customer=user.customer,
            date_ordered=guest_order.date_ordered,
            complete=guest_order.complete,
            transaction_id=guest_order.transaction_id,
            shipping_address=guest_order.shipping_address
        )

        for item in guest_order.items.all():
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity
            )
        
        guest_order.delete()

class Command(BaseCommand):
    help = 'Elimina GuestOrders incompletas y antiguas'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(days=1)  # o horas
        old_orders = GuestOrder.objects.filter(complete=False, date_ordered__lt=expiration_time)
        count = old_orders.count()
        old_orders.delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {count} GuestOrders antiguas e incompletas.'))


