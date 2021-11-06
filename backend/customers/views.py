from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product, Category, Inventory
from products.serializers import ProductSerializer, CategorySerializer
# Create your views here.


class AllProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AllCategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SpecificCategoryView(APIView):
    def get(self, request):
        category_name = request.data["category_name"]
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category_id=category.id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
