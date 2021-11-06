from django.contrib import admin
from .models import Customer, Order_Details, Wallet, Customer_Session
# Register your models here.

admin.site.register(Customer)
admin.site.register(Order_Details)
admin.site.register(Wallet)
admin.site.register(Customer_Session)
