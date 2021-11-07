from django.urls import path
from .views import AllCategoriesView, AllProductsView, SpecificCategoryView , CustomerAuthenticationView , CustomerSignUpView , CustomerOTPverification

urlpatterns = [
    path('allproducts/', AllProductsView.as_view()),
    path('allcategories/', AllCategoriesView.as_view()),
    path('specificcategory/', SpecificCategoryView.as_view()),
    path('login/', CustomerAuthenticationView.as_view()),
    path('signup/', CustomerSignUpView.as_view()),
    path('OTPverification/', CustomerOTPverification.as_view()),
]
