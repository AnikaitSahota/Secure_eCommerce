from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import Admin, Admin_Session , Admin_OTP
from entities import get_tokken , get_OTP
from datetime import datetime , timedelta , timezone
from hashlib import sha256
import json


# Create your views here.


class AdminSignUpView(APIView):  
	def post(self, request):
		if(not {'username' , 'email_id' , 'name' , 'password' , 'contact_number'}.issubset(request.data.keys())) :
			return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

		try :
			OTP = get_OTP()
			message = 'Hi ' + request.data['username'] + '\n' + 'Thanks for joining! Please verify your email address\n' + 'Use ' + str(OTP) + ' as OTP'
			print(message)
			# send_mail('Welcome to pappu ki dukan', 'Hi123412 This is your OTP, kindy do shit things with it' , settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])

			request.data['password'] = sha256(bytes(request.data['password'] , 'utf-8')).hexdigest()
			new_tuple = Admin_OTP(email_id = request.data['email_id'] , otp = OTP , meta_data = json.dumps(request.data))
			new_tuple.save()
			
		except :
			return Response({"status": "unsuccessfull"}, status=status.HTTP_200_OK)
		print('sending mail to', request.data['email_id'] , 'aka' , request.data['username'])
		return Response({"status": "success"}, status=status.HTTP_200_OK)

class AdminOTPverification(APIView) :
	def post(self, request) :
		if(not {'email_id' , 'OTP'}.issubset(request.data.keys())) :
			return Response({"status": "error" , "verification_message" : "wrong usages of API"}, status=status.HTTP_400_BAD_REQUEST)

		try :
			OTP_tuple = Admin_OTP.objects.get(email_id = request.data['email_id'])
			OTP_timestamp = OTP_tuple.time_of_creation
			OTP_metadata = json.loads(OTP_tuple.meta_data)
			if(OTP_tuple.otp == request.data['OTP']) :
				OTP_tuple.delete()
				if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes = settings.OTP_TIME_WINDOW)) :
					new_admin = Admin(username = OTP_metadata['username'], 
											name = OTP_metadata['name'], 
											email_id = OTP_metadata['email_id'], 
											password = OTP_metadata['password'],
											contact_number = OTP_metadata['contact_number'])
					new_admin.save()
					return Response({"status": "success" , "verification_message" : "email verified"}, status=status.HTTP_200_OK)
				else :
					raise Exception
			else :
				raise Exception
		except Exception as exp:
			print(exp)
			expired_OTP_tuples = Admin_OTP.objects.filter(time_of_creation__lt=(datetime.now(timezone.utc) - timedelta(minutes = settings.OTP_TIME_WINDOW)))
			expired_OTP_tuples.delete()
			
			return Response({"status": "unsuccessful" , "verification_message" : "wrong OTP"}, status=status.HTTP_200_OK)
		
		# return Response({"status": "unseccesfull" , "verification_message" : "wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)


class AdminAuthenticationView(APIView):	
	def post(self, request):
		if(not {'username' , 'password'}.issubset(request.data.keys())) :
			return Response({"status": "error"},
							status=status.HTTP_400_BAD_REQUEST)

		if (Admin.objects.filter(username=request.data['username'], password=sha256(bytes(request.data['password'] , 'utf-8')).hexdigest())).exists():

			current_token = get_tokken()
			admin = Admin.objects.get(username = request.data['username'])
			new_tuple = Admin_Session(admin = admin , token = current_token)
			new_tuple.save()

			return Response({"status": "success" , "token" : current_token},
							status=status.HTTP_200_OK)

		return Response({"status": "unsuccessful" },
                        status=status.HTTP_200_OK)
