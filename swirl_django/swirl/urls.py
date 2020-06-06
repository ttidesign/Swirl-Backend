from django.urls import path
from . import views
# from .views import item_list, item_detail
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('', views.ItemList.as_view(), name='item_list'),
    path('cart/', views.OrderItem.as_view(), name='order_item'),
    path('order-history/', views.Order.as_view(), name='order_history'),
    path('drinks/<int:pk>', views.item_detail, name='item_detail'),
    path('users', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
]