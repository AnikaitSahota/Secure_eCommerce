from django.contrib import admin
from .models import Admin, Admin_Session ,Admin_OTP
# Register your models here.

admin.site.register(Admin)
admin.site.register(Admin_Session)
admin.site.register(Admin_OTP)
