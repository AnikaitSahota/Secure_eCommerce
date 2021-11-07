# from django.shortcuts import render
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sellers.models import Seller, Seller_Session
from entities import get_tokken
# from . serializer import *
# from . models import *

class SellerAuthenticationView(APIView):
	
	# serializer_class = Login_authenticationSerializer
  
	# def get(self, request):
	# 	detail = [ {"name": detail.name,"detail": detail.detail} 
	# 	for detail in React.objects.all()]
	# 	return Response(detail)
  
	def post(self, request):
		# print(request.data , type(request.data))
		# serializer = Login_authenticationSerializer(data=request.data)
		# if serializer.is_valid():

		# print(request.session)
		# print({'username' , 'password'}.issubset(request.data.keys()))

		if(not {'username' , 'password'}.issubset(request.data.keys())) :
			return Response({"status": "error"},
							status=status.HTTP_400_BAD_REQUEST)

		if (Seller.objects.filter(username=request.data['username'], password=request.data['password'])).exists():

			current_token = get_tokken()
			seller = Seller.objects.get(username = request.data['username'])
			new_tuple = Seller_Session(seller = seller , token = current_token)
			new_tuple.save()

			return Response({"status": "success" , "token" : current_token},
							status=status.HTTP_200_OK)

		return Response({"status": "unsuccessful" },
                        status=status.HTTP_200_OK)


class CustomerAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)

class AdminAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)

class SuperAdminAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)
