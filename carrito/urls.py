from django.urls import path
from . import views

urlpatterns=[
    path('add', views.cart_view,name='add_to_cart'),
    # path('cart',views.cart,'cart')
]