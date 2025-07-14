from django.contrib import admin
from .models import Order, OrderItem, GuestOrder, GuestOrderItem
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(GuestOrderItem)
admin.site.register(GuestOrder)
