from django.urls import path
from . import views
from .views import AddToCartView, store, cart_detail, checkout
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('', views.ItemList.as_view(), name='item_list'),
    path('mycart/', views.OrderItem.as_view(), name='order_item'),
    path('order-history/', views.Order.as_view(), name='order_history'),
    path('drinks/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('users', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    # path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    #html render view
    #path('add-to-cart/<int:pk>', add_to_cart, name='add-to-cart'),
    path('products/', views.store, name='store'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('item_detail/<int:pk>', views.item_detail, name='item_detail'),
]