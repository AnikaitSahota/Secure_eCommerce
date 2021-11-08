from django.urls import path
# from .views import SellersView
from . import views

urlpatterns = [
    path('login/', views.AdminAuthenticationView.as_view()),
    path('signup/', views.AdminSignUpView.as_view()),
    path('OTPverification/', views.AdminOTPverification.as_view()),
    path('addCategory/', views.AddCategory.as_view()),
    path('get-admin-details/', views.GetAdminDetails.as_view()),
    path('update-admin-details/', views.UpdateAdminDetails.as_view()),
    path('get-sellers/', views.GetSellers.as_view()),
    path('verify-seller/', views.VerifySeller.as_view()),
    path('delete-seller/', views.DeleteSeller.as_view()),
    path('logout/', views.AdminLogoutView.as_view()),
]
