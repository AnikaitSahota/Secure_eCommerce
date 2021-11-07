from django.urls import path
from . import views

urlpatterns = [
    path('seller/', views.SellerSignUpView.as_view()),
    path('seller/OTPverification/', views.SellerOTPverification.as_view()),
    path('buyer/', views.CustomerSignUpView.as_view()),
    path('Admin/', views.AdminSignUpView.as_view()),
    # path('SuperAdmin/', views.SuperAdminSignUpView.as_view()),
]
