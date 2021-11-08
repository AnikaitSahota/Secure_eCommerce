from django.db import models
from sellers.models import Seller
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    img1 = models.TextField()
    img2 = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    price = models.DecimalField(max_digits=50, decimal_places=2)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
