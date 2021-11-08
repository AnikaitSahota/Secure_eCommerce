from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomerAuthenticationView.as_view()),
    path('signup/', views.CustomerSignUpView.as_view()),
    path('OTPverification/', views.CustomerOTPverification.as_view()),
    path('logout/', views.CustomerLogoutView.as_view()),
    path('buy-product/', views.BuyProduct.as_view()),
    path('update-wallet/', views.UpdateWallet.as_view()),
    path('get-customer-details/', views.GetCustomerDetails.as_view()),
    path('update-customer-details/', views.UpdateCustomerDetails.as_view()),
]
