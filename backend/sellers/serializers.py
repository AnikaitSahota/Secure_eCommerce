from rest_framework import serializers
from .models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            "username", "name", "email_id", "contact_number", "verified"
        )
