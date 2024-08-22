from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    address=models.CharField(max_length=255)
    contact=models.CharField(max_length=10)
    image=models.ImageField(blank=True, upload_to='image/')
                            
class Category(models.Model):
    cat=models.CharField(max_length=255)

class Product (models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    productname=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.IntegerField(null=True)
    quantity=models.IntegerField(null=True)
    img=models.ImageField(blank=True, upload_to='image/')
                      
class Cart (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price