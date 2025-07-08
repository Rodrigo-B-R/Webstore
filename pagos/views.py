from django.shortcuts import render
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from carrito.models import Order
from usuarios.models import ShippingAddress
from productos.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import get_object_or_404
from usuarios.models import ShippingAddress  

#maneja el pago con stripe
@login_required
def stripe_checkout_session(request, order_id):
    shipping_id = request.GET.get('shipping_id')

    order = get_object_or_404(Order, id=order_id, complete=False, customer=request.user.customer)

    #guardamos el shipping address seleccionado de esta orden
    if shipping_id:
        try:
            shipping_address = ShippingAddress.objects.get(id=shipping_id, customer=order.customer)
            order.shipping_address = shipping_address
            order.save()
        except ShippingAddress.DoesNotExist:
            return JsonResponse({'error': 'Dirección de envío inválida'}, status=400)

    line_items = []

    #por cada item lo prepara para usar stripe
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

    #crea un sesion de checkout de stripe 
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/pagos/success',
            cancel_url=f'http://127.0.0.1:8000/cart/checkout/?order_id={order.id}',
            metadata={'order_id': order.id}
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'id': checkout_session.id})


@login_required
def order_complete_view(request,order_id):

    order = get_object_or_404(Order, id=order_id, complete=False, customer= request.user.customer)

    order_items= order.orderitems_set.all()
    products= order.orderitems_set.all().product

    for product in products:
        product.stock -= order_items.quantity



    order.complete=True

    return render(request,'pagos/success.html')