from django.contrib import admin

# Register your models here.
from .models import Customer, ShippingAddress

admin.site.register(Customer)
admin.site.register(ShippingAddress)