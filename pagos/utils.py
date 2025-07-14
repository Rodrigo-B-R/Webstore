from django.shortcuts import redirect

def check_shipping_addres(order):
    if not order.shipping_address:
        return redirect('process_checkout', order_id=order.id)
    return