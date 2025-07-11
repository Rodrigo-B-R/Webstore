
def verificar_stock(order):
    items= order.orderitem_set.all()

    for item in items:
        if item.quantity <= item.product.stock:
            return True #falso si estamos comprando mas de lo que hay 
    return False


