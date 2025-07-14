from .models import Product

def get_product_or_redirect(product_id):
    try:
        product = Product.objects.get(id=product_id, visible=True)
        if product.stock < 1:
            product.visible = False
            product.save()
            return None
        return product
    except Product.DoesNotExist:
        return None
