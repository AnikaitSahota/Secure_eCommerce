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
        category_name = request.data["category_name"]
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category_id=category.id)
        serializer = ProductSerializerFew(products, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class SpecificProductView(APIView):
    def post(self, request):
        # product_id = request.GET['id']
        # if(product_id.isnumeric() == False):
        #     return Response({"status": "error"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        # product_id = int(product_id)

        # product = Product.objects.get(id=product_id)
        # serializer = ProductSerializer(product)
        # return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        print(request.data)
        product = Product.objects.get(id=request.data['id'])
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
        print(serializer)
        return Response({"status": "success", "data": serializer}, status=status.HTTP_200_OK)
