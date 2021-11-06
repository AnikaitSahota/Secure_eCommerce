from rest_framework import serializers
from .models import Seller


class NewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            "username", "name", "contact_number"
        )
