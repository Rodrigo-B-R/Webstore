from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

#Modela un cliente
class Customer(models.Model):

    
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name= models.CharField(max_length=200, null=True)
    


    def __str__(self):
        return self.name
    

#Modela una direccion de envio vinculada a un cliente
class ShippingAddress(models.Model):

    #clase hija de customer y order
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    
    #atributos
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address








    


    
