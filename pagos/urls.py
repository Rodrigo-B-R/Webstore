from django.urls import path
from . import  views


urlpatterns=[
    path('crear_pago/<int:order_id>/',views.stripe_checkout_session,name='crear_pago'),
    path('webhook/stripe/',views.stripe_webhook,name='stripe_webhook'),
    path('success',views.successful_payment_view,name='success')


    
    
]