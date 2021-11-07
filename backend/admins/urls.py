from django.urls import path
# from .views import SellersView
from . import views

urlpatterns = [
    path('login/', views.AdminAuthenticationView.as_view()),
    path('signup/', views.AdminSignUpView.as_view()),
    path('OTPverification/', views.AdminOTPverification.as_view()),
]
