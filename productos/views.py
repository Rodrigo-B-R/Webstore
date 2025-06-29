from django.shortcuts import render, get_object_or_404
import os
from .models import Product

# Create your views here.


def main_page_view(request):

    products= Product.objects.all()

    context={'products':products}




    return render(request,'productos/main_page.html',context=context)



def product_view(request,id):

    product= get_object_or_404(Product, id=id)
    context={'product':product}

    return render(request,'productos/product.html',context=context)

