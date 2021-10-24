from django.urls import path
from . import views

urlpatterns = [
    path('seller/', views.SellerAuthenticationView.as_view()),
    path('buyer/', views.BuyerAuthenticationView.as_view()),
    path('Admin/', views.AdminAuthenticationView.as_view()),
    path('SuperAdmin/', views.SuperAdminAuthenticationView.as_view()),
]
