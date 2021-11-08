from django.urls import path
from . import views
urlpatterns = [
    path('allproducts/', views.AllProductsView.as_view()),
    path('allcategories/', views.AllCategoriesView.as_view()),
    path('specificcategory/', views.SpecificCategoryView.as_view()),
    path('login/', views.CustomerAuthenticationView.as_view()),
    path('signup/', views.CustomerSignUpView.as_view()),
    path('OTPverification/', views.CustomerOTPverification.as_view()),
    path('buy-product/', views.CustomerOTPverification.as_view()),
]
