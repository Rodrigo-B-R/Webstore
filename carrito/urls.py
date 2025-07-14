from django.urls import path
from . import views, viewss

urlpatterns=[
     path('view', views.cart_view,name='cart'),
     path('delete/<int:item_id>',views.delete_item_view,name='delete_item'),
     path('update_quantity/<int:product_id>/',views.update_quantity_view,name='update_quantity'),
     path('checkout/<int:order_id>',views.checkout_view,name='checkout'),
     path('checkout/process/<int:order_id>', views.proccess_checkout,name='process_checkout')
 ]



# urlpatterns=[
#     path('view', viewss.cart_view,name='cart'),
#     path('delete/<int:item_id>',viewss.delete_item_view,name='delete_item'),
#     path('update_quantity/<int:product_id>/',viewss.update_quantity_view,name='update_quantity'),
#     path('checkout/<int:order_id>',viewss.checkout_view,name='checkout'),
#     path('checkout/process/<int:order_id>', viewss.proccess_checkout,name='process_checkout')
# ]