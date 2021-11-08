from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Seller, Seller_Session, Seller_OTP
from products.models import Product, Category, Inventory
from products.serializers import ProductSerializerFew, CategorySerializerFew, ProductSerializer
from .serializers import SellerSerializer
from rest_framework import status
from entities import get_OTP, get_tokken
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
        seller = Seller.objects.get(username=request.data["username"])
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
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        products = Product.objects.filter(seller=seller,
                                          category=Category.objects
                                          .get(name=request.data['category_name']))
        serializer = ProductSerializerFew(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ViewProduct(APIView):
    def post(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        product = Product.objects.get(id=request.data['id'])
        product_dict = {'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'category': product.category.name,
                        'inventory': product.inventory.quantity,
                        'price': str(product.price),
                        }
        serializer = json.dumps(product_dict)
        print(serializer)
        return Response({"status": "success", "data": serializer}, status=status.HTTP_200_OK)


class EditProduct(APIView):
    def put(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        product = Product.objects.get(id=request.data['id'])
        if 'description' in request.data:
            product.description = request.data['description']
        if 'inventory' in request.data:
            inventory = Inventory.objects.get(product_name=product.name)
            inventory.quantity = request.data['inventory']
            inventory.save()
        if 'price' in request.data:
            product.price = request.data['price']
        product.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class GetAllCategories(APIView):
    def post(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
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
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if (not is_verified(seller, request)):
            return Response({"status": "Seller Not Verified"}, status=status.HTTP_200_OK)
        name = request.data['name']
        try:
            inventory = Inventory.objects.get(product_name=name)
            new_product = Product(name=name,
                                  seller=seller,
                                  description=request.data['description'],
                                  category=Category.objects.get(
                                      name=request.data['category']),
                                  inventory=inventory,
                                  price=request.data['price'])
            new_product.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as exp:
            print(exp)
            new_inventory = Inventory(
                product_name=name, quantity=request.data['inventory'])
            new_inventory.save()
            new_product = Product(name=name,
                                  seller=seller,
                                  description=request.data['description'],
                                  category=Category.objects.get(
                                      name=request.data['category']),
                                  inventory=new_inventory,
                                  price=request.data['price'])
            new_product.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)


class GetSellerDetails(APIView):
    def post(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        serializer = SellerSerializer(seller)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class UpdateSellerDetails(APIView):
    def put(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        if ('name' in request.data):
            seller.name = request.data['name']
        if ('contact_number' in request.data):
            seller.contact_number = request.data['contact_number']
        seller.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class SellerSignUpView(APIView):
    def post(self, request):
        if(not {'username', 'email_id', 'name',
                'password', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            OTP = get_OTP()
            message = 'Hi ' + request.data['username'] + '\n' + \
                'Thanks for joining! Please verify your email address\n' + \
                'Use ' + str(OTP) + ' as OTP'
            print(message)
            # try:
            #     send_mail('Welcome to pappu ki dukan', 'Hi123412 This is your OTP, kindy do shit things with it',
            #               settings.DEFAULT_FROM_EMAIL, [request.data['email_id']])
            # except Exception as exp:
            #     print(exp)
            #     return Response({"status": "Invalid Email"}, status=status.HTTP_200_OK)

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
        status_msg = 'success'
        if(not {'email_id', 'OTP'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            OTP_tuple = Seller_OTP.objects.get(
                email_id=request.data['email_id'])
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
            expired_OTP_tuples = Seller_OTP.objects.filter(time_of_creation__lt=(
                datetime.now(timezone.utc) - timedelta(minutes=settings.OTP_TIME_WINDOW)))
            expired_OTP_tuples.delete()
            return Response({"status": status_msg}, status=status.HTTP_200_OK)


class SellerAuthenticationView(APIView):
    def post(self, request):
        if(not {'username', 'password'}.issubset(request.data.keys())):
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (Seller.objects.filter(username=request.data['username'],
                                  password=sha256(bytes(request.data['password'], 'utf-8')).hexdigest())).exists():

            current_token = get_tokken()
            seller = Seller.objects.get(username=request.data['username'])
            new_tuple = Seller_Session(seller=seller, token=current_token)
            new_tuple.save()

            return Response({"status": "success", "token": current_token},
                            status=status.HTTP_200_OK)

        return Response({"status": "User Not Found"}, status=status.HTTP_200_OK)


class SellerLogoutView(APIView):
    def post(self, request):
        print(request.data)
        seller = Seller.objects.get(username=request.data["username"])
        if (not verify_token(seller, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        seller_sessions = Seller_Session.objects.filter(seller=seller)
        seller_sessions.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
