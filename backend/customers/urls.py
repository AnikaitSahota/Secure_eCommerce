from django.urls import path
from .views import AllCategoriesView, AllProductsView

urlpatterns = [
    path('allproducts', AllProductsView.as_view()),
    path('allcategories', AllCategoriesView.as_view())
]
