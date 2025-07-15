from django.urls import path
from . import views

urlpatterns=[
     path('view', views.cart_view,name='cart'),
     path('delete/<int:item_id>',views.delete_item_view,name='delete_item'),
     path('update_quantity/<int:product_id>/',views.update_quantity_view,name='update_quantity'),
     path('checkout/<int:order_id>',views.checkout_view,name='checkout'),
     path('checkout/process/<int:order_id>', views.process_checkout_view,name='process_checkout')
 ]
