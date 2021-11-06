from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .models import Admin, Admin_Session
# Create your views here.


class AdminSignUpView(APIView):
    def post(self, request):
        if(not {'user_name', 'email_id'}.issubset(request.data.keys())):
            send_mail('verification for pappu ki dukan',
                      '123412 This is your OTP, kindy do shit things with ',
                      settings.DEFAULT_FROM_EMAIL, [request.email_id])

            return Response({"status": "error", "verification_message": "OTP verification stage"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success", "verification_message": "random_val"},
                        status=status.HTTP_200_OK)


class AdminAuthenticationView(APIView):
    def post(self, request):
        print(request.data.keys())
        print({'user_name', 'pass_hash'}.issubset(request.data.keys()))

        if(not {'user_name', 'pass_hash'}.issubset(request.data.keys())):
            return Response({"status": "error", "verification_status": "False"},
                            status=status.HTTP_400_BAD_REQUEST)

        username = request.data["user_name"]
        password = request.data['pass_hash']
        if (Admin.objects.filter(username=username, password=password)).exists():
            return Response({"status": "success", "verification_status": "True"},
                            status=status.HTTP_200_OK)
        return Response({"status": "unsuccessful", "verification_status": "False"},
                        status=status.HTTP_200_OK)
