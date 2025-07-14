from usuarios.models import ShippingAddress

def check_stock(request,order):
    if request.user.is_authenticated:
        items= order.orderitem_set.all()
    else:
        items=order.items.all()

    for item in items:
        if item.quantity <= item.product.stock:
            return True #falso si estamos comprando mas de lo que hay 
    return False



def get_or_create_shipping_address(customer, cleaned_data):
    """
    Devuelve una dirección de envío existente si coincide con los datos proporcionados,
    o crea una nueva si no existe.

    Parámetros:
        customer (Customer): el cliente autenticado.
        cleaned_data (dict): datos validados del formulario.

    Retorna:
        ShippingAddress: la dirección existente o recién creada.
    """
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


