# from django.shortcuts import render
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

		print(request.data.keys())
		print({'user_name' , 'pass_hash'}.issubset(request.data.keys()))

		if(not {'user_name' , 'pass_hash'}.issubset(request.data.keys())) :
			return Response({"status": "error" , "verification_status" : "False"}, status=status.HTTP_400_BAD_REQUEST)

		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)

class BuyerAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)

class AdminAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)

class SuperAdminAuthenticationView(APIView):
	def post(self, request):
		return Response({"status": "success", "verification_status" : "True"}, status=status.HTTP_200_OK)