from django.forms import ModelForm
from usuarios.models import Customer, ShippingAddress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms


#Formulario de usuario
class UserForm(UserCreationForm):
    email=  forms.EmailField(required=True)

    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']

#formulario de cliente
class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields=['name']

#formulario de direccion
class ShippingAddressForm(ModelForm):
    class Meta:
        model= ShippingAddress
        fields=['address','city','state','zipcode']








