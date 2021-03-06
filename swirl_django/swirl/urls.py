from django.urls import path
from . import views
from .views import  store, item_detail, checkout ,cart_detail,updateItem, processOrdder, home, store_map, favorite_list
# from .views import  updateItem
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('api/drinks', views.ItemList.as_view(), name='item_list'),
    path('api/cart/', views.OrderItemDRF.as_view(), name='order_item'),
    # path('order-history/', views.OrderDRF.as_view(), name='order_history'),
    path('api/drinks/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('api/users/', views.UserList.as_view(), name='user_list'),
    path('api/users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('api/customers/', views.CustomerList.as_view(), name='customer_list'),
    path('api/customers/<int:pk', views.CustomerDetail.as_view(), name='customer_detail'),
    path('', views.home, name='home'),
    path('products/', views.store, name='store'),
    path('products/<int:pk>', views.item_detail, name='item_detail'),
    path('locations/', views.store_map, name='store_map'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrdder, name='process_order'),
]