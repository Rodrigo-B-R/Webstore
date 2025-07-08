from django.urls import path
from . import  views


urlpatterns=[
    path('crear_pago/<int:order_id>/',views.stripe_checkout_session,name='crear_pago')


    
    
]