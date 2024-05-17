from django.urls import path

from .views import *

urlpatterns = [
    path("",HomeView.as_view(), name="home"),
    path("item/<int:pk>/",ItemView.as_view(), name="item"),
    path("cart/<int:pk>/",CartView.as_view(), name="cart"),
    path("delete_cart_item/<int:pk>/", DeleteCartItemView.as_view(), name="delete_cart_item"),
    path("cart_update/<int:pk>/", CartUpdateView.as_view(), name="cart_update"),    
    path("order/",OrderView.as_view(), name="order"),
    path("success/",SuccessView.as_view(), name="success"),
]