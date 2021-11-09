from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Seller, Seller_Session, Seller_OTP
from products.models import Product, Category
from products.serializers import ProductSerializerFew, CategorySerializerFew
from .serializers import SellerSerializer
from rest_framework import status
from django.db.models import Q
from entities import get_OTP, get_tokken, username_verification, password_verification
from datetime import datetime, timedelta, timezone
from django.conf import settings
import json
from hashlib import sha256


def is_verified(seller, request):
    if (not seller.verified):
        return False
    return True


def verify_token(seller, request):
    front_token = request.data['token']
    seller_sessions = Seller_Session.objects.filter(seller=seller)
    for session in seller_sessions:
        session_timestamp = session.time_of_creation
        if ((front_token == session.token) and ((datetime.now(timezone.utc) - session_timestamp) <= timedelta(hours=settings.SESSION_TIME_WINDOW))):
            return True
    return False
# Create your views here.


class GetAllProducts(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        products = Product.objects.filter(seller=seller)
        serializer = ProductSerializerFew(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetSpecificProducts(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'category_name'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        try:
            category = Category.objects.get(name=request.data['category_name'])
        except:
            return Response({"status": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        products = Product.objects.filter(seller=seller, category=category)
        serializer = ProductSerializerFew(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ViewProduct(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'id'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        try:
            product = Product.objects.get(id=request.data['id'])
        except:
            return Response({"status": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        product_dict = {'id': product.id,
                        'name': product.name,
                        'img1': product.img1,
                        'img2': product.img2,
                        'description': product.description,
                        'category': product.category.name,
                        'inventory': product.inventory,
                        'price': str(product.price),
                        }
        serializer = json.dumps(product_dict)
        print(serializer)
        return Response({"status": "success", "data": serializer}, status=status.HTTP_200_OK)


class EditProduct(APIView):
    def put(self, request):
        print(request.data)
        if(not {'username', 'token', 'id', 'description',
                'inventory', 'price', 'img1', 'img2'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        try:
            product = Product.objects.get(id=request.data['id'])
        except:
            return Response({"status": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        product.description = request.data['description']
        product.inventory = request.data['inventory']
        product.price = request.data['price']
        product.img1 = request.data['img1']
        product.img2 = request.data['img2']
        product.save(update_fields=['description',
                     'inventory', 'price', 'img1', 'img2'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class GetAllCategories(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        categories = Category.objects.all()
        serializer = CategorySerializerFew(categories, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class AddProduct(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'name', 'img1', 'img2',
                'description', 'category', 'inventory', 'price'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        name = request.data['name']
        new_product = Product(name=name,
                              img1=request.data['img1'],
                              img2=request.data['img2'],
                              seller=seller,
                              description=request.data['description'],
                              category=Category.objects.get(
                                  name=request.data['category']),
                              inventory=request.data['inventory'],
                              price=request.data['price'])
        new_product.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class GetSellerDetails(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        serializer = SellerSerializer(seller)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UpdateSellerDetails(APIView):
    def put(self, request):
        print(request.data)
        if(not {'username', 'token', 'name', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        seller.name = request.data['name']
        seller.contact_number = request.data['contact_number']
        seller.save(update_fields=['name', 'contact_number'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class SellerSignUpView(APIView):
    def post(self, request):
        if(not {'username', 'email_id', 'name',
                'password', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (username_verification(request.data['username']))):
            return Response({"status": "Username doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (password_verification(request.data['password']))):
            return Response({"status": "Password doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (Seller.objects.filter(Q(name=request.data['username']) |
                                  Q(email_id=request.data['email_id']) |
                                  Q(contact_number=request.data['contact_number'])).exists()):
            return Response({"status": "Admin with this username, email_id or contact_number already exists!"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            OTP = get_OTP()
            message = 'Hi ' + request.data['username'] + '\n' + \
                'Thanks for joining! Please verify your email address\n' + \
                'Use ' + str(OTP) + ' as OTP'
            # print(message)
            try:
                send_mail('Welcome to pappu ki dukan', message,
                          settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
            except Exception as exp:
                print(exp)
                return Response({"status": "Invalid Email"}, status=status.HTTP_200_OK)

            request.data['password'] = sha256(
                bytes(request.data['password'], 'utf-8')).hexdigest()
            try:
                new_tuple = Seller_OTP(
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


class SellerOTPverification(APIView):
    def post(self, request):
        print(request.data)
        status_msg = 'success'
        if(not {'email_id', 'OTP'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        expired_OTP_tuples = Seller_OTP.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.OTP_TIME_WINDOW)))
        expired_OTP_tuples.delete()
        try:
            OTP_tuple = Seller_OTP.objects.filter(
                email_id=request.data['email_id']).order_by('-time_of_creation')[0]
            print(OTP_tuple)
            OTP_timestamp = OTP_tuple.time_of_creation
            OTP_metadata = json.loads(OTP_tuple.meta_data)
            if(OTP_tuple.otp == request.data['OTP']):
                OTP_tuple.delete()
                if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes=settings.OTP_TIME_WINDOW)):
                    new_seller = Seller(username=OTP_metadata['username'],
                                        name=OTP_metadata['name'],
                                        email_id=OTP_metadata['email_id'],
                                        password=OTP_metadata['password'],
                                        contact_number=OTP_metadata['contact_number'])
                    new_seller.save()
                    return Response({"status": status_msg},
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


class SellerAuthenticationView(APIView):
    def post(self, request):
        if(not {'username', 'password'}.issubset(request.data.keys())):
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (Seller.objects.filter(username=request.data['username'],
                                  password=sha256(bytes(request.data['password'], 'utf-8')).hexdigest())).exists():

            current_token = get_tokken()
            try:
                seller = Seller.objects.get(username=request.data['username'])
            except Exception as exp:
                print(exp)
                return Response({"status": "error"},
                                status=status.HTTP_400_BAD_REQUEST)

            new_tuple = Seller_Session(seller=seller, token=current_token)
            new_tuple.save()

            return Response({"status": "success", "token": current_token},
                            status=status.HTTP_200_OK)

        return Response({"status": "User Not Found"}, status=status.HTTP_200_OK)


class SellerLogoutView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seller = Seller.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Seller not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        try:
            seller_session = Seller_Session.objects.get(
                seller=seller, token=request.data['token'])
        except Exception as exp:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        seller_session.delete()
        expired_sessions = Seller_Session.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.SESSION_TIME_WINDOW)))
        expired_sessions.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
