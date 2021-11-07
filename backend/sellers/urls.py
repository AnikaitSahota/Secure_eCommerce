from django.urls import path
# from .views import SellersView
from . import views

urlpatterns = [
    path('login/', views.SellerAuthenticationView.as_view()),
    path('signup/', views.SellerSignUpView.as_view()),
    path('OTPverification/', views.SellerOTPverification.as_view()),
]
