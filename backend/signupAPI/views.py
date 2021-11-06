from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
# from ./../entities 
# from . serializer import *
# from . models import *


# def get_OTP() :
# 	re


class SellerSignUpView(APIView):
	
	# serializer_class = Login_authenticationSerializer
  
	# def get(self, request):
	# 	detail = [ {"name": detail.name,"detail": detail.detail} 
	# 	for detail in React.objects.all()]
	# 	return Response(detail)
  
	def post(self, request):
		# print(request.data , type(request.data))

		if(not {'user_name' , 'email_id'}.issubset(request.data.keys())) :
			return Response({"status": "error" , "verification_message" : "wrong usages of API"}, status=status.HTTP_400_BAD_REQUEST)

		try :
			send_mail('verification for pappu ki dukan', '123412 This is your OTP, kindy do shit things with it' , settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
		except :
			return Response({"status": "error", "verification_message" : "invalid email id"}, status=status.HTTP_200_OK)
		print('sending mail to', request.data['email_id'] , 'aka' , request.data['user_name'])
		return Response({"status": "success", "verification_message" : "OTP verification stage"}, status=status.HTTP_200_OK)

# class SignUpView(APIView):
	
# 	# serializer_class = Login_authenticationSerializer
  
# 	# def get(self, request):
# 	# 	detail = [ {"name": detail.name,"detail": detail.detail} 
# 	# 	for detail in React.objects.all()]
# 	# 	return Response(detail)
  
# 	def post(self, request):
# 		# print(request.data , type(request.data))

# 		if(not {'user_name' , 'pass_hash'}.issubset(request.data.keys())) :
# 			return Response({"status": "error" , "verification_tokken" : "abcd_damn_this_is_tocken"}, status=status.HTTP_400_BAD_REQUEST)

# 		return Response({"status": "success", "verification_tokken" : "random_val"}, status=status.HTTP_200_OK)


class BuyerSignUpView(APIView):
	def post(self, request):
		if(not {'user_name' , 'email_id'}.issubset(request.data.keys())) :
			send_mail('verification for pappu ki dukan', '123412 This is your OTP, kindy do shit things with ' , settings.DEFAULT_FROM_EMAIL, [request.email_id])

			return Response({"status": "error" , "verification_message" : "OTP verification stage"}, status=status.HTTP_400_BAD_REQUEST)

		return Response({"status": "success", "verification_message" : "random_val"}, status=status.HTTP_200_OK)

class AdminSignUpView(APIView):
	def post(self, request):
		if(not {'user_name' , 'email_id'}.issubset(request.data.keys())) :
			send_mail('verification for pappu ki dukan', '123412 This is your OTP, kindy do shit things with ' , settings.DEFAULT_FROM_EMAIL, [request.email_id])

			return Response({"status": "error" , "verification_message" : "OTP verification stage"}, status=status.HTTP_400_BAD_REQUEST)

		return Response({"status": "success", "verification_message" : "random_val"}, status=status.HTTP_200_OK)
