from django.urls import path
from . import views

urlpatterns=[
     path('view', views.cart_view_router,name='cart'),
     path('delete/<int:item_id>',views.delete_item_router,name='delete_item'),
     path('update_quantity/<int:product_id>/',views.update_quantity_router,name='update_quantity'),
     path('checkout/<int:order_id>',views.checkout_view_router,name='checkout'),
     path('checkout/process/<int:order_id>', views.process_checkout_router,name='process_checkout')
 ]
