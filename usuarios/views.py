from django.shortcuts import render
from .forms import ShippingAddressForm, UserForm, CustomerForm
from django.contrib.auth.decorators import login_required
from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from usuarios.models import Customer



# Create your views here.

#formulario de login
def login_view(request):
    if request.method=='POST':
        form= AuthenticationForm(request, data=request.POST) #formulario de django para autentificacion
        if form.is_valid():
            user= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user= authenticate(request, username=user, password=password) #autentifia al usuario
            if user is not None:
                login(request, user) #inicia sesion del usuario 
                return redirect('profile')
    else:
        form= AuthenticationForm()
    
    return render (request, 'usuarios/login.html',context={'login_form':form})


#formulario de registro
def signup_view(request):

    if request.method== 'POST':
        user_form= UserForm(request.POST)
        customer_form= CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user=user_form.save()
            customer= customer_form.save(commit= False)
            customer.user= user
            customer.save() 
            #guarda cliente y usuario

            login(request, user)
            return redirect('profile')
    else:
        user_form= UserForm()
        customer_form= CustomerForm()
    
    context={'user_form':user_form, 'customer_form': customer_form}
    
    return render (request, "usuarios/signup.html", context=context)


#cerrar sesion 
@login_required
def logout_view(request):


    logout(request)

    return redirect('login')


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
            #guarda la direccion
    else:
        shipping_form= ShippingAddressForm
    
    return render(request, 'usuarios/shippingAddress.html' ,context={'shipping_form':shipping_form})


