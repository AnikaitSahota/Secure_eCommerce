from django.urls import path
# from .views import SellersView
from . import views

urlpatterns = [
    path('login/', views.SellerAuthenticationView.as_view()),
    path('signup/', views.SellerSignUpView.as_view()),
    path('OTPverification/', views.SellerOTPverification.as_view()),
    path('logout/', views.SellerLogoutView.as_view()),
    path('get-products/', views.GetAllProducts.as_view()),
    path('get-categories/', views.GetAllCategories.as_view()),
    path('add-product/', views.AddProduct.as_view()),
    path('view-product/', views.ViewProduct.as_view()),
    path('edit-product/', views.EditProduct.as_view()),
    path('get-specific-products/', views.GetSpecificProducts.as_view()),
    path('get-seller-details/', views.GetSellerDetails.as_view()),
    path('update-seller-details/', views.UpdateSellerDetails.as_view()),
]
