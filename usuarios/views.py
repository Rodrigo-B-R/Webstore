from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms 
from .forms import ShippingAddressForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from usuarios.models import Customer, ShippingAddress



# Create your views here.




#formulario de registro



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

#formulario de direccion

@login_required
def shippingAddress_view(request):
    if request.method== 'POST':

        shipping_form= ShippingAddressForm(request.POST)
        if shipping_form.is_valid():
            shipping_address=shipping_form.save( commit= False )
            shipping_address.customer= request.user.customer
            shipping_address.save()
            return redirect('profile')
            #guarda la direccion
    else:
        shipping_form= ShippingAddressForm
    
    return render(request, 'usuarios/shippingAddress.html' ,context={'shipping_form':shipping_form})

#editar direcciones de envio 
def edit_adress_view(request,id):

    
    customer= request.user.customer

    address= get_object_or_404(ShippingAddress,pk=id,customer=customer)

    #cuando se envia el formulario con los datos nuevos
    if request.method== 'POST':

        shipping_form= ShippingAddressForm(request.POST, instance=address) #el formulario cambia el adress actual
        
        if shipping_form.is_valid():
            shipping_address=shipping_form.save( commit= False )
            shipping_address.customer= customer
            shipping_address.save()
            #guarda la direccion
            return redirect('profile')
    else:
        #cuando apenas vamos a editar los datos 
        shipping_form= ShippingAddressForm(instance=address)

    context={'shipping_form':shipping_form,'mode':'edit'}

    

    

    return render(request,'usuarios/shippingAddress.html',context)


@login_required
def delete_address_view(request,id):

    if request.method =='POST':
        address= get_object_or_404(ShippingAddress,pk=id,customer=request.user.customer)
        address.delete()

    return redirect('profile')
