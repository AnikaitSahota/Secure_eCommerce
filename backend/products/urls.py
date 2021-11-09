from django.urls import path
from .views import AllCategoriesView, AllProductsView, SpecificCategoryView, SpecificProductView

urlpatterns = [
    path('all-products/', AllProductsView.as_view()),
    path('all-categories/', AllCategoriesView.as_view()),
    path('specific-category/', SpecificCategoryView.as_view()),
    path('specific-product/', SpecificProductView.as_view()),
]
