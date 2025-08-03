from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from . models import Customer
from utils import link_guest_orders_to_user





@receiver(user_logged_in)
@receiver(user_signed_up)
def handle_user_login(sender,user,request, **kwargs):
    customer, created = Customer.objects.get_or_create(
        user=user,
        defaults={"name": user.get_full_name()}
    )

    link_guest_orders_to_user(user)