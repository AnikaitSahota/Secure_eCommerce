from django.urls import path
from .views import AllCategoriesView, AllProductsView, SpecificCategoryView , SpecificProductView

urlpatterns = [
    path('allproducts/', AllProductsView.as_view()),
    path('allcategories/', AllCategoriesView.as_view()),
    path('specificcategory/', SpecificCategoryView.as_view()),
    path('specificproduct/', SpecificProductView.as_view()),
]
