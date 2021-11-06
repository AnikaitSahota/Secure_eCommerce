from django.urls import path
from .views import AllCategoriesView, AllProductsView, SpecificCategoryView

urlpatterns = [
    path('allproducts', AllProductsView.as_view()),
    path('allcategories', AllCategoriesView.as_view()),
    path('specificcategory', SpecificCategoryView.as_view())
]
