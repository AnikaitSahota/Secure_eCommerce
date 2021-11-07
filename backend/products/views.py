from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Inventory
from .serializers import ProductSerializer, CategorySerializer
# from django.conf import settings
# Create your views here.

# PRODUCT_PAGE_SIZE = 10


class ProductsView(APIView):
	def post(self, request):
		pass

	def get(self, request):
		products = Product.objects.all()
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)


class AllProductsView(APIView):
	def get(self, request):
		# if('page_number' in request.GET) :
		# 	page_num = request.GET['page_number']
		# else :
		# 	page_num = '0' 
		
		# if(page_num.isnumeric() == False) :
		# 	return Response({"status": "error"},
		# 					status=status.HTTP_400_BAD_REQUEST)

		# page_num = int(page_num)
		# products = Product.objects.all()[PRODUCT_PAGE_SIZE * page_num : PRODUCT_PAGE_SIZE * (page_num+1) -1]
		# print(len(Product.objects.all()))
		products = Product.objects.all()
		serializer = ProductSerializer(products, many=True)
		return Response({'status' : 'success', 'data' : serializer.data} , status=status.HTTP_200_OK)


class AllCategoriesView(APIView):
	def get(self, request):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response({'status' : 'success', 'data' : serializer.data} , status=status.HTTP_200_OK)


class SpecificCategoryView(APIView):
	def get(self, request):
		category_name = request.data["category_name"]
		category = Category.objects.get(name=category_name)
		products = Product.objects.filter(category_id=category.id)
		serializer = ProductSerializer(products, many=True)
		return Response({'status' : 'success', 'data' : serializer.data} , status=status.HTTP_200_OK)



class SpecificProductView(APIView) :
	def get(self, request) :
		if('product_id' in request.GET) :
			product_id = request.GET['product_id']
		else :
			product_id = '1' 
		
		if(product_id.isnumeric() == False) :
			return Response({"status": "error"},
							status=status.HTTP_400_BAD_REQUEST)

		product_id = int(product_id)
		product = Product.objects.get(id = product_id)
		serializer = ProductSerializer(product)
		return Response({'status' : 'success', 'data' : serializer.data} , status=status.HTTP_200_OK)
