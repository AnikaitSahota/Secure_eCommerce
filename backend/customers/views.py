from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from .models import Customer, Customer_Session, Customer_OTP, Order_Details, Wallet
from .serializers import CustomerSerializer, OrderSerializer
from products.serializers import ProductSerializerFew
from rest_framework import status
from entities import get_tokken, get_OTP, username_verification, password_verification
from django.db.models import Q
from datetime import datetime, timedelta, timezone
from django.db.models import F
from django.conf import settings
import json
from decimal import Decimal
from hashlib import sha256
from django.core.mail import send_mail


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
        print(request.data)
        if (not {'username', 'token', 'amount'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        amount = Decimal(request.data['amount'])
        try:
            customer_wallet = Wallet.objects.get(customer=customer)
        except Exception as exp:
            print(exp)
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        customer_wallet.amount += amount
        if (customer_wallet.amount < 0):
            customer_wallet.amount = 0
        customer_wallet.save(update_fields=['amount'])
        return Response({"status": "success", "balance": customer_wallet.amount}, status=status.HTTP_200_OK)


class SearchProducts(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'search_query'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        search_query = request.data['search_query']
        products = Product.objects.filter(Q(name__icontains=search_query) |
                                          Q(category__name__icontains=search_query))
        serializer = ProductSerializerFew(products, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)


class BuyProduct(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token', 'id', 'quantity'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        try:
            product = Product.objects.get(id=request.data['id'])
        except:
            return Response({"status": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        quantity = int(request.data['quantity'])
        total_amount = (product.price * quantity)
        try:
            wallet = Wallet.objects.get(customer=customer)
        except Exception as exp:
            print(exp)
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        wallet_amount = wallet.amount
        if (wallet_amount >= total_amount):
            current_quantity = product.inventory
            if (current_quantity >= quantity):
                product.inventory = current_quantity - quantity
                product.save(update_fields=['inventory'])
                wallet.amount = wallet_amount - total_amount
                wallet.save(update_fields=['amount'])
                new_order = Order_Details(product_name=product.name,
                                          customer=customer,
                                          quantity=quantity,
                                          description=('Purchased ' + str(quantity) + ' pieces of ' + product.name +
                                                       ' sold by ' + product.seller.username + ' for $' + str(total_amount)),
                                          total_amount=total_amount)
                new_order.save()
                return Response({"status": "success", "balance": wallet.amount}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Insufficient Inventory, Try Again Later"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Insufficient Balance, Add balance to your wallet"}, status=status.HTTP_200_OK)


class OrderHistory(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        past_orders = Order_Details.objects.filter(customer=customer)
        serializer = OrderSerializer(past_orders, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetCustomerDetails(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        serializer = CustomerSerializer(customer)
        try:
            wallet = Wallet.objects.get(customer=customer)
        except Exception as exp:
            print(exp)
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": serializer.data, "balance": wallet.amount}, status=status.HTTP_200_OK)


class UpdateCustomerDetails(APIView):
    def put(self, request):
        print(request.data)
        if(not {'username', 'token', 'name', 'contact_number', 'address'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        customer.name = request.data['name']
        customer.contact_number = request.data['contact_number']
        customer.address = request.data['address']
        customer.save(update_fields=['name', 'contact_number', 'address'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class CustomerSignUpView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'email_id', 'name', 'address',
                'password', 'contact_number'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (username_verification(request.data['username']))):
            return Response({"status": "Username doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (not (password_verification(request.data['password']))):
            return Response({"status": "Password doesn't meet the requirements"}, status=status.HTTP_400_BAD_REQUEST)
        if (Customer.objects.filter(Q(name=request.data['username']) |
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
        print(request.data)
        status_msg = 'success'
        if(not {'email_id', 'OTP'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        expired_OTP_tuples = Customer_OTP.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.OTP_TIME_WINDOW)))
        expired_OTP_tuples.delete()
        try:
            OTP_tuple = Customer_OTP.objects.filter(
                email_id=request.data['email_id']).order_by('-time_of_creation')[0]
            print(OTP_tuple)
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
                    wallet = Wallet(customer=new_customer, amount=1000)
                    wallet.save()
                    return Response({"status": status_msg}, status=status.HTTP_200_OK)
                else:
                    status_msg = 'OTP has Expired'
                    raise Exception  # OTP has expired
            else:
                status_msg = 'Wrong OTP'
                raise Exception  # wrong OTP
        except Exception as exp:
            print(exp)
            return Response({"status": status_msg}, status=status.HTTP_200_OK)


class CustomerAuthenticationView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'password'}.issubset(request.data.keys())):
            return Response({"status": "error"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (Customer.objects.filter(username=request.data['username'],
                                    password=sha256(bytes(request.data['password'], 'utf-8')).hexdigest())).exists():

            current_token = get_tokken()
            try:
                customer = Customer.objects.get(
                    username=request.data['username'])
            except Exception as exp:
                print(exp)
                return Response({"status": "error"},
                                status=status.HTTP_400_BAD_REQUEST)
            new_tuple = Customer_Session(
                customer=customer, token=current_token)
            new_tuple.save()

            return Response({"status": "success", "token": current_token},
                            status=status.HTTP_200_OK)

        return Response({"status": "User Not Found"}, status=status.HTTP_200_OK)


class CustomerLogoutView(APIView):
    def post(self, request):
        print(request.data)
        if(not {'username', 'token'}.issubset(request.data.keys())):
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(username=request.data["username"])
        except Exception as exp:
            print(exp)
            return Response({"status": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        if (not verify_token(customer, request)):
            return Response({"status": "Unsuccessful"}, status=status.HTTP_200_OK)
        customer_sessions = Customer_Session.objects.filter(customer=customer)
        customer_sessions.delete()
        expired_sessions = Customer_Session.objects.filter(time_of_creation__lt=(
            datetime.now(timezone.utc) - timedelta(minutes=settings.SESSION_TIME_WINDOW)))
        expired_sessions.delete()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
