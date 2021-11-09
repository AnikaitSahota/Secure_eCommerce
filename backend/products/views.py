from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializerFew, CategorySerializerFew
import json
# from django.conf import settings
# Create your views here.


class AllProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializerFew(products, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class AllCategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializerFew(categories, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class SpecificCategoryView(APIView):
    def post(self, request):
        if(not {'category_name'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            category = Category.objects.get(
                name=request.data["category_name"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializerFew(products, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class SpecificProductView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'id'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        product_id = request.data['id']
        if(product_id.isnumeric() == False):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        product_id = int(product_id)
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({"status": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        product_dict = {'id': product.id,
                        'name': product.name,
                        'img1': product.img1,
                        'img2': product.img2,
                        'seller': product.seller.username,
                        'description': product.description,
                        'category': product.category.name,
                        'inventory': product.inventory,
                        'price': str(product.price),
                        }
        serializer = json.dumps(product_dict)
        return Response({"status": "success", "data": serializer}, status=status.HTTP_200_OK)
