from django.urls import path
from . import views
# from .views import item_list, item_detail
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('', views.ItemList.as_view(), name='item_list'),
    path('cart/', views.OrderItem.as_view(), name='order_list'),
    path('drinks/<int:pk>', views.item_detail, name='item_detail'),
]