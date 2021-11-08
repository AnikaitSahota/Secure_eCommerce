from django.db import models
from sellers.models import Seller
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField()
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-price']

    def __str__(self):
        return self.name
