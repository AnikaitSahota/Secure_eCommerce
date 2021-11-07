from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from products.models import Product, Category, Inventory
# from products.serializers import ProductSerializer, CategorySerializer
from .models import Customer , Customer_Session , Customer_OTP
from rest_framework import status
from entities import get_tokken , get_OTP
from datetime import datetime , timedelta , timezone
from django.conf import settings
import json
from hashlib import sha256
# Create your views here.



class CustomerAuthenticationView(APIView):
	def post(self, request):

		if(not {'username' , 'password'}.issubset(request.data.keys())) :
			return Response({"status": "error"},
							status=status.HTTP_400_BAD_REQUEST)

		if (Customer.objects.filter(username=request.data['username'], password=sha256(bytes(request.data['password'] , 'utf-8')).hexdigest())).exists():

			current_token = get_tokken()
			customer = Customer.objects.get(username = request.data['username'])
			new_tuple = Customer_Session(customer = customer , token = current_token)
			new_tuple.save()

			return Response({"status": "success" , "token" : current_token},
							status=status.HTTP_200_OK)

		return Response({"status": "unsuccessful" },
						status=status.HTTP_200_OK)


# class CustomerLogoutView(APIView):
# 	def post(self, request):
		# todo : logout / remove the session-token 
		# return Response({"status": "error"},
		# 					status=status.HTTP_400_BAD_REQUEST)


		# if(not {'username' , 'token'}.issubset(request.data.keys())) :
		# 	return Response({"status": "error"},
		# 					status=status.HTTP_400_BAD_REQUEST)

		# if(Customer.objects.filter(username=request.data['username'], token=request.data['token'])).exists():
		# 	seller = Customer.objects.get(username = request.data['username'])
		# 	new_tuple = Customer_Session(seller = seller , token = current_token)
		# 	new_tuple.save()

		# 	return Response({"status": "success" , "token" : current_token},
		# 					status=status.HTTP_200_OK)

		# return Response({"status": "unsuccessful" },
		#                 status=status.HTTP_200_OK)


class CustomerSignUpView(APIView):  
	def post(self, request):
		# print(request.data , type(request.data))

		if(not {'username' , 'email_id' , 'name' , 'address' , 'password' , 'contact_number'}.issubset(request.data.keys())) : # TODO : add other fields
			return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

		try :
			OTP = get_OTP()
			message = 'Hi ' + request.data['username'] + '\n' + 'Thanks for joining! Please verify your email address\n' + 'Use ' + str(OTP) + ' as OTP'
			print(message)
			# send_mail('Welcome to pappu ki dukan', 'Hi123412 This is your OTP, kindy do shit things with it' , settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
			request.data['password'] = sha256(bytes(request.data['password'] , 'utf-8')).hexdigest()
			new_tuple = Customer_OTP(email_id = request.data['email_id'] , otp = OTP , meta_data = json.dumps(request.data))
			new_tuple.save()
		except Exception as exp :
			print(exp)
			return Response({"status": "unsuccessfull"}, status=status.HTTP_200_OK)
		print('sending mail to', request.data['email_id'] , 'aka' , request.data['username'])
		return Response({"status": "success"}, status=status.HTTP_200_OK)

class CustomerOTPverification(APIView) :
	def post(self, request) :
		if(not {'email_id' , 'OTP'}.issubset(request.data.keys())) :
			return Response({"status": "error" , "verification_message" : "wrong usages of API"}, status=status.HTTP_400_BAD_REQUEST)

		# print(request.data)
		try :
			OTP_tuple = Customer_OTP.objects.get(email_id = request.data['email_id'])
			# if(not OTP_tuple.exists()) :
			# 	return Response({"status": "unseccesfull" , "verification_message" : "no email-match"}, status=status.HTTP_200_OK)

			OTP_timestamp = OTP_tuple.time_of_creation
			OTP_metadata = json.loads(OTP_tuple.meta_data)
			if(OTP_tuple.otp == request.data['OTP']) :
				OTP_tuple.delete()
				if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes = settings.OTP_TIME_WINDOW)) :
					new_customer = Customer(username = OTP_metadata['username'], 
											name = OTP_metadata['name'], 
											email_id = OTP_metadata['email_id'], 
											password = OTP_metadata['password'],
											address = OTP_metadata['address'],
											contact_number = OTP_metadata['contact_number'])
					new_customer.save()
					return Response({"status": "success" , "verification_message" : "email verified"}, status=status.HTTP_200_OK)
				else :
					raise Exception			# email found but OTP expired
			else :
				raise Exception 			# email found but OTP not match
		except Exception as exp:
			print(exp)

			expired_OTP_tuples = Customer_OTP.objects.filter(time_of_creation__lt=(datetime.now(timezone.utc) - timedelta(minutes = settings.OTP_TIME_WINDOW)))
			expired_OTP_tuples.delete()

			return Response({"status": "unsuccessful" , "verification_message" : "wrong OTP"}, status=status.HTTP_200_OK)
		
		# return Response({"status": "unseccesfull" , "verification_message" : "wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
