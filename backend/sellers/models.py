from django.db import models

# Create your models here.


class Seller(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=50, unique=True)
    verified = models.BooleanField(default=False)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Seller_OTP(models.Model):
    email_id = models.CharField(max_length=50)
    otp = models.CharField(max_length=10)
    meta_data = models.CharField(max_length=500)
    time_of_creation = models.DateTimeField(auto_now_add=True)


class Seller_Session(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    time_of_creation = models.DateTimeField(auto_now_add=True)
