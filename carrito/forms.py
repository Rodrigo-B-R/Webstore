from django.forms import ModelForm
from .models import OrderItem, GuestOrder, GuestOrderItem
from django import forms


class OrderItemForm(ModelForm):

    class Meta:
        model=OrderItem
        fields=['quantity']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',  # HTML: evita negativos en el navegador
        })
        self.fields['quantity'].min_value = 1


class GuestCheckoutForm(forms.Form):
    email= forms.EmailField(label='Correo electronico')

    
class GuestOrderItemForm(ModelForm):

    class Meta:
        model=GuestOrderItem
        fields=['quantity']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',  # HTML: evita negativos en el navegador
        })
        self.fields['quantity'].min_value = 1