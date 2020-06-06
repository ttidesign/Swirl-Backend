from django.urls import path
from . import views
from .views import item_list, item_detail
urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('drinks/<int:pk>', views.item_detail, name='item_detail'),
]