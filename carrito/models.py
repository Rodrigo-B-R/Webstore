from django.db import models
from django.core.validators import MinValueValidator
import uuid


# Create your models here.

class Order(models.Model):
    #clase hija de customer
    customer = models.ForeignKey('usuarios.Customer', on_delete=models.SET_NULL, null=True, blank=True) 

    #atributos
    date_ordered= models.DateField(auto_now_add=True)
    complete= models.BooleanField(default=False)
    transaction_id= models.CharField(max_length=100 , null=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction_id= str(uuid.uuid4())

    def __str__(self):
        return f"Orden #{self.id} - {self.customer.name if self.customer else 'Invitado'}"  
    
    #metodos
    @property
    def get_cart_total(self):
        return sum([item.get_total for item in self.orderitem_set.all()]) 
        #itera por los objetos orderitem y suma sus precios
    
    #numero de items en la orden 
    @property
    def get_cart_items(self):
        return sum([item.quantity for item in self.orderitem_set.all()])
    
#Modela un producto dentro de una orden
class OrderItem(models.Model):

    #relacionada con producto y orden 
    product = models.ForeignKey('productos.Product', on_delete=models.SET_NULL, null=True) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    #atributos
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(auto_now_add=True)

    #metodos
    @property
    def get_total(self):
        return self.product.price * self.quantity
    
 