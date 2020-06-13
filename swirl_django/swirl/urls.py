from django.urls import path
from . import views
from .views import  store, item_detail, checkout ,cart_detail,updateItem, processOrdder, home
# from .views import  updateItem
from rest_framework.routers import DefaultRouter
urlpatterns = [
    # path('', views.ItemList.as_view(), name='item_list'),
    # path('mycart/', views.OrderItem.as_view(), name='order_item'),
    # path('order-history/', views.Order.as_view(), name='order_history'),
    # path('drinks/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    # path('users/', views.UserList.as_view(), name='user_list'),
    # path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    # path('customers/', views.CustomerList.as_view(), name='customer_list'),
    # path('customers/<int:pk', views.CustomerDetail.as_view(), name='customer_detail'),
    path('', views.home, name='home'),
    path('products/', views.store, name='store'),
    path('products/<int:pk>', views.item_detail, name='item_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrdder, name='process_order'),
]