from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from . models import Customer
from utils import link_guest_orders_to_user


@receiver(user_signed_up)
def create_customer_signup(sender,request,user, **kwargs):
    Customer.objects.get_or_create(user=user,name=user.get_full_name())
    


@receiver(user_logged_in)
def create_customer_login(sender,request,user,**kwargs):
    Customer.objects.get_or_create(user=user,name=user.get_full_name())


@receiver(user_logged_in)
@receiver(user_signed_up)
def handle_user_login(sender,user,request, **kwargs):
    link_guest_orders_to_user(user)