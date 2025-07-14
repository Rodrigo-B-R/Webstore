from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms 
from .forms import ShippingAddressForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from usuarios.models import Customer, ShippingAddress



# Create your views here.

#cerrar sesion 

@login_required
def logout_view(request):


    logout(request)


    return redirect('account_login')


#vista de perfil
@login_required
def profile_view(request):
    
    try:
        customer = request.user.customer

        shipping_addresses = customer.shippingaddress_set.all()
    except customer.DoesNotExist:
        customer = None
        shipping_addresses = []

    context={"user":request.user,"customer":customer,'shipping_addresses':shipping_addresses }

    return render (request,"usuarios/profile.html",context=context)


@login_required
def delete_address_view(request,id):

    if request.method =='POST':
        address= get_object_or_404(ShippingAddress,pk=id,customer=request.user.customer)
        address.delete()

    return redirect('profile')
