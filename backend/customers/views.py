from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product, Category, Inventory
from products.serializers import ProductSerializer, CategorySerializer
from .models import Customer, Customer_Session, Customer_OTP, Wallet
from rest_framework import status
from entities import get_tokken, get_OTP
from datetime import datetime, timedelta, timezone
from django.conf import settings
import json
from hashlib import sha256


def verify_token(customer, request):
    front_token = request.data['token']
    customer_sessions = Customer_Session.objects.filter(customer=customer)
    for session in customer_sessions:
        session_timestamp = session.time_of_creation
        if ((front_token == session.token) and ((datetime.now(timezone.utc) - session_timestamp) <= timedelta(hours=settings.SESSION_TIME_WINDOW))):
            return True
    return False

# Create your views here.


class UpdateWallet(APIView):
    def post(self, request):
        amount = request.data['amount']
        if (not verify_token(request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        customer_username = request.data["username"]
        customer = Customer.objects.get(username=customer_username)
        customer_wallet = Wallet.objects.get(customer=customer)
        customer_wallet.amount = amount
        customer_wallet.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class BuyProduct(APIView):
    def post(self, request):
        if (not verify_token(request)):
            return Response({"status": "unsuccessful"}, status=status.HTTP_200_OK)
        customer = Customer.objects.get(username=request.data["username"])
        product = Product.objects.get(id=request.data['id'])
        quantity = request.data['quantity']
        amount = product.price * quantity
        wallet = Wallet(customer=customer)
        if (wallet.amount >= amount):
            inventory = Inventory.objects.get(product_name=product.name)
            if (inventory.quantity >= quantity):
                inventory.quantity -= quantity
                inventory.save()
                wallet.amount -= amount
                wallet.save()
                return Response({"status": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Insufficient Inventory, Try Again Later"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Insufficient Balance, Add balance to your wallet"}, status=status.HTTP_200_OK)


class AllProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class AllCategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SpecificCategoryView(APIView):
    def get(self, request):
        category_name = request.data["category_name"]
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category_id=category.id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CustomerSignUpView(APIView):
    def post(self, request):
        if(not {'username', 'email_id', 'name', 'address',
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
                new_tuple = Customer_OTP(
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


class CustomerOTPverification(APIView):
    def post(self, request):
        status_msg = 'success'
        if(not {'email_id', 'OTP'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            OTP_tuple = Customer_OTP.objects.get(
                email_id=request.data['email_id'])
            OTP_timestamp = OTP_tuple.time_of_creation
            OTP_metadata = json.loads(OTP_tuple.meta_data)
            if(OTP_tuple.otp == request.data['OTP']):
                OTP_tuple.delete()
                if(datetime.now(timezone.utc) - OTP_timestamp <= timedelta(minutes=settings.OTP_TIME_WINDOW)):
                    new_customer = Customer(username=OTP_metadata['username'],
                                            name=OTP_metadata['name'],
                                            email_id=OTP_metadata['email_id'],
                                            password=OTP_metadata['password'],
                                            address=OTP_metadata['address'],
                                            contact_number=OTP_metadata['contact_number'])
                    new_customer.save()
                    return Response({"status": status_msg}, status=status.HTTP_200_OK)
                else:
                    status_msg = 'OTP has Expired'
                    raise Exception  # OTP has expired
            else:
                status_msg = 'Wrong OTP'
                raise Exception  # wrong OTP
        except Exception as exp:
            print(exp)
            expired_OTP_tuples = Customer_OTP.objects.filter(time_of_creation__lt=(
                datetime.now(timezone.utc) - timedelta(minutes=settings.OTP_TIME_WINDOW)))
            expired_OTP_tuples.delete()
            return Response({"status": status_msg}, status=status.HTTP_200_OK)


class CustomerAuthenticationView(APIView):
    def post(self, request):

        if(not {'username', 'password'}.issubset(request.data.keys())):
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (Customer.objects.filter(username=request.data['username'],
                                    password=sha256(bytes(request.data['password'], 'utf-8')).hexdigest())).exists():

            current_token = get_tokken()
            customer = Customer.objects.get(username=request.data['username'])
            new_tuple = Customer_Session(
                customer=customer, token=current_token)
            new_tuple.save()

            return Response({"status": "success", "token": current_token},
                            status=status.HTTP_200_OK)

        return Response({"status": "User Not Found"}, status=status.HTTP_200_OK)


class CustomerLogoutView(APIView):
    def post(self, request):
        print(request.data)
        customer = Customer.objects.get(username=request.data["username"])
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        customer_sessions = Customer_Session.objects.filter(customer=customer)
        customer_sessions.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
