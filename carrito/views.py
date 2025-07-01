from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


from .models import OrderItem, Order
from .forms import OrderItemForm
from productos.models import Product

# Create your views here.





def cart_view(request):

    return render(request, 'carrito/cart.html')
