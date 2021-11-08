from rest_framework import serializers
from .models import Product, Category, Inventory


class ProductSerializerFew(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', "name", "description"
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializerFew(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name", "description"
        )
