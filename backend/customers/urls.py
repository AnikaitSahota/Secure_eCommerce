from django.urls import path
from .views import CustomerAuthenticationView , CustomerSignUpView , CustomerOTPverification

urlpatterns = [
    path('login/', CustomerAuthenticationView.as_view()),
    path('signup/', CustomerSignUpView.as_view()),
    path('OTPverification/', CustomerOTPverification.as_view()),
]
