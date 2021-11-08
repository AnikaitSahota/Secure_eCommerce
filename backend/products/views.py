from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
from .serializers import CategorySerializer

# Create your views here.


class AllCategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
