from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from entities import get_OTP
from sellers.models import Seller_OTP
from datetime import datetime , timezone , timedelta
# from ./../entities 
# from . serializer import *
# from . models import *

class SellerSignUpView(APIView):
	
	# serializer_class = Login_authenticationSerializer
  
	# def get(self, request):
	# 	detail = [ {"name": detail.name,"detail": detail.detail} 
	# 	for detail in React.objects.all()]
	# 	return Response(detail)
  
	def post(self, request):
		# print(request.data , type(request.data))

		if(not {'username' , 'email_id'}.issubset(request.data.keys())) :
			return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

		try :
			OTP = get_OTP()
			message = 'Hi ' + request.data['username'] + '\n' + 'Thanks for joining! Please verify your email address\n' + 'Use ' + str(OTP) + ' as OTP'
			print(message)
			# send_mail('Welcome to pappu ki dukan', 'Hi123412 This is your OTP, kindy do shit things with it' , settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
			new_tuple = Seller_OTP(email_id = request.data['email_id'] , otp = OTP)
			new_tuple.save()
			
		except :
			return Response({"status": "unsuccessfull"}, status=status.HTTP_200_OK)
		print('sending mail to', request.data['email_id'] , 'aka' , request.data['username'])
		return Response({"status": "success"}, status=status.HTTP_200_OK)

class SellerOTPverification(APIView) :
	def post(self, request) :
		# return Response({"status": "error" , "verification_message" : "wrong usages of API"}, status=status.HTTP_400_BAD_REQUEST)

		if(not {'email_id' , 'OTP'}.issubset(request.data.keys())) :
			return Response({"status": "error" , "verification_message" : "wrong usages of API"}, status=status.HTTP_400_BAD_REQUEST)

		print(request.data)
		try :
			OTP_tuple = Seller_OTP.objects.get(email_id = request.data['email_id'])
			# print(OTP_tuple.time_of_creation  , type(OTP_tuple.time_of_creation))
			OTP_timestamp = OTP_tuple.time_of_creation
			# print(datetime.utcnow())
			# print(datetime.now() - OTP_tuple.time_of_creation)
			if(OTP_tuple.otp == request.data['OTP']) :
				# return Response({"status": "success" , "verification_message" : "email verified"}, status=status.HTTP_200_OK)
				# print(datetime.now() - OTP_tuple.time_of_creation)
				OTP_tuple.delete()
				# print('delete tuple')
				if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes = settings.OTP_TIME_WINDOW)) :
					
					return Response({"status": "success" , "verification_message" : "email verified"}, status=status.HTTP_200_OK)
				else :
					raise Exception
					# return Response({"status": "un success" , "verification_message" : "time passed"}, status=status.HTTP_200_OK)
			else :
				raise Exception
		except :
			# print(exp)
			# TODO : cleaning of OTP table
			return Response({"status": "unseccesfull" , "verification_message" : "wrong OTP"}, status=status.HTTP_200_OK)
		
		# return Response({"status": "unseccesfull" , "verification_message" : "wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)




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


class CustomerSignUpView(APIView):
    def post(self, request):
        if(not {'user_name', 'email_id'}.issubset(request.data.keys())):
            send_mail('verification for pappu ki dukan', '123412 This is your OTP, kindy do shit things with ',
                      settings.DEFAULT_FROM_EMAIL, [request.email_id])

            return Response({"status": "error", "verification_message": "OTP verification stage"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success", "verification_message": "random_val"}, status=status.HTTP_200_OK)


class AdminSignUpView(APIView):
    def post(self, request):
        if(not {'user_name', 'email_id'}.issubset(request.data.keys())):
            send_mail('verification for pappu ki dukan', '123412 This is your OTP, kindy do shit things with ',
                      settings.DEFAULT_FROM_EMAIL, [request.email_id])

            return Response({"status": "error", "verification_message": "OTP verification stage"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success", "verification_message": "random_val"}, status=status.HTTP_200_OK)
