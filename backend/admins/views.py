from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Admin, Admin_Session, Admin_OTP
from products.models import Category, Product
from customers.models import Customer
from entities import get_tokken, get_OTP, password_verification, username_verification
from datetime import datetime, timedelta, timezone
from .serializers import AdminSerializer
from sellers.serializers import SellerSerializer
from sellers.models import Seller
from hashlib import sha256
import json


def is_verified(admin, request):
    if (not admin.verified):
        return False
    return True


def verify_token(admin, request):
    front_token = request.data['token']
    admin_sessions = Admin_Session.objects.filter(admin=admin)
    for session in admin_sessions:
        session_timestamp = session.time_of_creation
        if ((front_token == session.token) and ((datetime.now(timezone.utc) - session_timestamp) <= timedelta(hours=settings.SESSION_TIME_WINDOW))):
            return True
    return False
# Create your views here.


class GetSellers(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class VerifySeller(APIView):
    def put(self, request):
        print(request.data)
        if(not {'username', 'token', 'sellerUsername'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        try:
            seller = Seller.objects.get(
                username=request.data['sellerUsername'])
        except:
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        seller.verified = True
        seller.save(update_fields=['verified'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class DeleteSeller(APIView):
    def delete(self, request):
        print(request.data)
        if(not {'username', 'token', 'sellerUsername'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        try:
            seller = Seller.objects.get(
                username=request.data['sellerUsername'])
        except:
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        seller.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class DeleteCustomer(APIView):
    def delete(self, request):
        print(request.data)
        if(not {'username', 'token', 'customerUsername'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        try:
            customer = Customer.objects.get(
                username=request.data['customerUsername'])
        except:
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        customer.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class AddCategory(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'name', 'description'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        name = request.data['name']
        description = request.data['description']
        new_category = Category(name=name, description=description)
        new_category.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class DeleteCategory(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'category_name'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        try:
            category = Category.objects.get(name=request.data['category_name'])
        except:
            return Response({"status": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        category.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class DeleteProduct(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'id'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(admin, request)):
            return Response({"status": "Admin Not Verified"}, status=status.HTTP_200_OK)
        try:
            product = Product.objects.get(id=request.data['id'])
        except:
            return Response({"status": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class GetAdminDetails(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        serializer = AdminSerializer(admin)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UpdateAdminDetails(APIView):
    def put(self, request):
        print(request.data)
        if(not {'username', 'token', 'name', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        admin.name = request.data['name']
        admin.contact_number = request.data['contact_number']
        admin.save(update_fields=['name', 'contact_number'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class AdminSignUpView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'email_id', 'name',
                'password', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (username_verification(request.data['username']))):
            return Response({"status": "Username doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (password_verification(request.data['password']))):
            return Response({"status": "Password doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (Admin.objects.filter(Q(name=request.data['username']) |
                                 Q(email_id=request.data['email_id']) |
                                 Q(contact_number=request.data['contact_number'])).exists()):
            return Response({"status": "Admin with this username, email_id or contact_number already exists!"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            OTP = get_OTP()
            message = 'Hi ' + request.data['username'] + '\n' + \
                'Thanks for joining! Please verify your email address\n' + \
                'Use ' + str(OTP) + ' as OTP'
            print(message)
            try:
                send_mail('Welcome to pappu ki dukan', message,
                          settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
            except Exception as exp:
                print(exp)
                return Response({"status": "Invalid Email"}, status=status.HTTP_200_OK)

            request.data['password'] = sha256(
                bytes(request.data['password'], 'utf-8')).hexdigest()
            try:
                new_tuple = Admin_OTP(
                    email_id=request.data['email_id'], otp=OTP, meta_data=json.dumps(request.data))
                new_tuple.save()
                print('sending mail to',
                      request.data['email_id'], 'aka', request.data['username'])
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            except Exception as exp:
                print(exp)
                return Response({"status": "Username Already Used"}, status=status.HTTP_200_OK)
        except Exception as exp:
            print(exp)
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)


class AdminOTPverification(APIView):
    def post(self, request):
        print(request.data)
        status_msg = 'success'
        if(not {'email_id', 'OTP'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        expired_OTP_tuples = Admin_OTP.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.OTP_TIME_WINDOW)))
        expired_OTP_tuples.delete()
        try:
            OTP_tuple = Admin_OTP.objects.filter(
                email_id=request.data['email_id']).order_by('-time_of_creation')[0]
            print(OTP_tuple)
            OTP_timestamp = OTP_tuple.time_of_creation
            OTP_metadata = json.loads(OTP_tuple.meta_data)
            if(OTP_tuple.otp == request.data['OTP']):
                OTP_tuple.delete()
                if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes=settings.OTP_TIME_WINDOW)):
                    new_admin = Admin(username=OTP_metadata['username'],
                                      name=OTP_metadata['name'],
                                      email_id=OTP_metadata['email_id'],
                                      password=OTP_metadata['password'],
                                      contact_number=OTP_metadata['contact_number'])
                    new_admin.save()
                    return Response({"status": "success", "verification_message": "email verified"},
                                    status=status.HTTP_200_OK)
                else:
                    status_msg = 'OTP has Expired'
                    raise Exception  # OTP has expired
            else:
                status_msg = 'Wrong OTP'
                raise Exception  # wrong OTP
        except Exception as exp:
            print(exp)
            return Response({"status": status_msg}, status=status.HTTP_200_OK)


class AdminAuthenticationView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'password'}.issubset(request.data.keys())):
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (Admin.objects.filter(username=request.data['username'],
                                 password=sha256(bytes(request.data['password'], 'utf-8')).hexdigest())).exists():

            current_token = get_tokken()
            try:
                admin = Admin.objects.get(username=request.data['username'])
            except:
                return Response({"status": "error"},
                                status=status.HTTP_400_BAD_REQUEST)
            new_tuple = Admin_Session(admin=admin, token=current_token)
            new_tuple.save()

            return Response({"status": "success", "token": current_token},
                            status=status.HTTP_200_OK)

        return Response({"status": "User Not Found"}, status=status.HTTP_200_OK)


class AdminLogoutView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(admin, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        admin_sessions = Admin_Session.objects.filter(admin=admin)
        admin_sessions.delete()
        expired_sessions = Admin_Session.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.SESSION_TIME_WINDOW)))
        expired_sessions.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
