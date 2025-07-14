from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage

    
#Modela Productos 
class Product(models.Model):
    name= models.CharField(max_length=200)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description= models.TextField(null=True, blank= True)
    visible= models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image= models.ImageField(upload_to='productos/', storage=MediaCloudinaryStorage(),null=True, blank=True)
    upladed_at= models.DateField(auto_now_add=True)

