from usuarios.models import ShippingAddress
from carrito.models import Order,OrderItem, GuestOrder,GuestOrderItem
from django.shortcuts import get_object_or_404
from productos.models import Product

def check_stock(request,order):
    
    items=order.items.all()

    for item in items:
        if item.quantity <= item.product.stock:
            return True #falso si estamos comprando mas de lo que hay 
    return False

def get_item(request, lookup_id, order, by='product', create_if_missing=False):
    
    if request.user.is_authenticated:
        if by == 'product':
            product = get_object_or_404(Product, id=lookup_id)
            item, created = OrderItem.objects.get_or_create(order=order, product=product)
            return item
        elif by == 'item':
            return get_object_or_404(OrderItem, id=lookup_id, order=order)
    else:
        if by == 'product':
            product = get_object_or_404(Product, id=lookup_id)
            try:
                item = GuestOrderItem.objects.get(order=order, product=product)
            except GuestOrderItem.DoesNotExist:
                if create_if_missing:
                    item = GuestOrderItem.objects.create(order=order, product=product, quantity=1)
                else:
                    raise
            return item
        elif by == 'item':
            return get_object_or_404(GuestOrderItem, id=lookup_id, order=order)


def get_or_create_shipping_address(customer, cleaned_data):

    # Extrae los campos clave del formulario
    address = cleaned_data.get('address')
    city = cleaned_data.get('city')
    postal_code = cleaned_data.get('postal_code')

    # Verifica si ya existe una dirección idéntica para ese cliente
    existing = ShippingAddress.objects.filter(
        customer=customer,
        address=address,
        city=city,
        postal_code=postal_code
    ).first()

    if existing:
        return existing

    # Si no existe, crea una nueva (no la guarda aquí)
    new_address = ShippingAddress(
        customer=customer,
        address=address,
        city=city,
        postal_code=postal_code
    )
    new_address.save()
    return new_address


