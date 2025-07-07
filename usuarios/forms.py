from django.forms import ModelForm
from usuarios.models import Customer, ShippingAddress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django import forms


#Formulario de usuario
class UserForm(UserCreationForm):
    email=  forms.EmailField(required=True)

    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#formulario de cliente
class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields=['name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#formulario de direccion
class ShippingAddressForm(ModelForm):
    class Meta:
        model= ShippingAddress
        fields=['address','city','state','zipcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#Formulario custom de login para añadir estilos 
class CustomLoginForm(AuthenticationForm):
    
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})










