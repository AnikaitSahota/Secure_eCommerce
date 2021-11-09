from rest_framework import serializers
from .models import Customer, Order_Details


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "username", "name", "email_id", "contact_number", "address"
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Details
        fields = (
            "product_name", 'quantity', 'total_amount', 'time_of_creation'
        )
