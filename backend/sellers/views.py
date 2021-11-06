from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Seller
from .serializers import SellerSerializer, NewProductSerializer

# Create your views here.


class SellersView(APIView):
    def post(self, request):
        serializer = NewProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return HttpResponse("Error")
        return HttpResponse("Product Added")

    def get(self, request):
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data)
