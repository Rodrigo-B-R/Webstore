from django.forms import ModelForm
from .models import OrderItem

class OrderItemForm(ModelForm):

    class Meta:
        model=OrderItem
        fields=['quantity']


