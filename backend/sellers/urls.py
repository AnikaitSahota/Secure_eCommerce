from django.urls import path
from .views import SellersView

urlpatterns = [
    path('', SellersView.as_view())
]
