from rest_framework import serializers
from .models import Product, Category


class ProductSerializerFew(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', "name", "description", 'img1'
        )


class CategorySerializerFew(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
        )
