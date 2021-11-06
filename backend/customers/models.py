from django.db import models

# Create your models here.


class Customer(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=50)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Order_Details(models.Model):
    product_name = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.CharField(max_length=500)
    total_amount = models.DecimalField(max_digits=50, decimal_places=2)
    time_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.time_of_creation + ": " + self.total_amount


class Wallet(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer + ": " + self.amount


class Customer_OTP(models.Model):
    email_id = models.CharField(max_length=50)
    otp = models.CharField(max_length=10)
    time_of_creation = models.DateTimeField(auto_now_add=True)


class Customer_Session(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    time_of_creation = models.DateTimeField(auto_now_add=True)
