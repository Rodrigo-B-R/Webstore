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
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import get_object_or_404
from usuarios.models import ShippingAddress  




#maneja el pago con stripe
@login_required
def stripe_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id, complete=False, customer=request.user.customer)

    # Verifica que tenga dirección de envío asignada
    if not order.shipping_address:
        return redirect('process_checkout', order_id=order.id)

    # Verifica stock
    if not check_stock(request,order):
        return redirect('cart')

    # Construir line_items para Stripe
    line_items = []
    for item in order.orderitem_set.all():
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
            success_url=f'http://127.0.0.1:8000/pagos/success?order_id={order.id}',
            cancel_url=f'http://127.0.0.1:8000/cart/checkout/?order_id={order.id}',
            metadata={'order_id': order.id}
        )
    except Exception as e:
        print("Error con Stripe:", e)
        return redirect('cart')

    # Redirigir directamente al checkout de Stripe
    return redirect(checkout_session.url)




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

        # if session['payment_status'] == 'paid':
        order = get_object_or_404(Order, id=order_id, complete=False)

            # ✅ Actualizamos el stock y marcamos como completa
        for item in order.orderitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

        order.complete = True
        order.date_ordered= timezone.now()
        order.save()

    return HttpResponse(status=200)


@login_required
def successful_payment_view(request):

    order_id=request.GET.get('order_id')


    try:
        order= Order.objects.get(complete=True, customer= request.user.customer,id=order_id)
    except:   
        return render(request, 'pagos/success.html', {'message': 'No se encontró una orden completada.'})
    
    order_items= order.orderitem_set.all()
    for order in order_items:
        if order.product.stock < 1:
            order.product.visible=False
    
    context={'order':order, 'order_items': order.orderitem_set.all()}

    return render(request,'pagos/success.html', context)


# def guest_checkout(request):
#     form= GuestCheckoutForm()
#     if form.is_valid():
#         email=form.cleaned_data['email']

