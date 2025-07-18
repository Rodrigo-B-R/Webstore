from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from carrito.models import Order
from usuarios.models import ShippingAddress
from productos.models import Product
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from carrito.utils import check_stock
from .utils import check_shipping_addres
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import get_object_or_404
from usuarios.models import ShippingAddress  
from carrito.models import GuestOrder,GuestOrderItem

from .utils import get_order, get_order_by_id, update_order


#1
def stripe_checkout_session(request,order_id):
    order= get_order(request,order_id)

    check_shipping_addres(order)

    if not check_stock(request,order):
        return redirect('cart')
    
    items= order.items.all()
    
    return create_stripe_session(items, order)


#3
def create_stripe_session(items,order):
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'mxn',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    # Crear sesión de Stripe
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'webstore-xb8n.onrender.com/pagos/success?order_id={order.id}',
            cancel_url=f'webstore-xb8n.onrender.com/cart/checkout/?order_id={order.id}',
            metadata={'order_id': order.id}
        )
    except Exception as e:
        print("Error con Stripe:", e)
        return redirect('cart')

    # Redirigir directamente al checkout de Stripe
    return redirect(checkout_session.url)


#4
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # La añades en settings
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)  # payload inválido
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # firma inválida

    # Solo actuamos cuando Stripe confirma pago exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']
        if session['payment_status'] == 'paid':

            
            order=get_order_by_id(order_id=order_id)

            update_order(order)

        return HttpResponse(status=200)
    
def successful_payment_view(request):

    order_id=request.GET.get('order_id')


    try:
        order= get_order(request,order_id=order_id,is_complete=True)
    except:   
        return render(request, 'pagos/success.html', {'message': 'No se encontró una orden completada.'})
    
    order_items= order.items.all()
    for item in order_items:
        if item.product.stock < 1:
            item.product.visible=False
            item.product.save()
    
    context={'order':order, 'order_items': order_items}

    return render(request,'pagos/success.html', context)
