from django.contrib import admin
from .models import Seller, Seller_Session , Seller_OTP
# Register your models here.

admin.site.register(Seller)
admin.site.register(Seller_Session)
admin.site.register(Seller_OTP)
