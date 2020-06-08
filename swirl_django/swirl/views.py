from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST 
from .serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
# Create your views here.



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderItem(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class Order(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@permission_classes((permissions.AllowAny,))
class AddToCartView(APIView):
    def post(self,request):
        pk = request.data.get('id',None)
        if pk is None:
            return Response({'message':'Invalid request'}, status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item, pk=item.pk)
        order_item, created = OrderItem.objects.get_or_create(item=item,
        user=request.user,
            ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            #check if there is any item in order
            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity +=1
                order_item.save()
                return Response(status=HTTP_200_OK)
            else: 
                order.item.add(order_item)
                return Response(status=HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return Response(status=HTTP_200_OK)
        
def add_to_cart(request,pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item,
    user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if there is any item in order
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity +=1
            order_item.save()
        else: 
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect('item_detail',pk=item.pk)

def store(request):
    items = Item.objects.all()
    return render(request, 'swirl/store.html',{'items':items})

def item_detail(request,pk):
    item = Item.objects.get(id=pk)
    return render(request, 'swirl/item_detail.html',{'item':item})

def checkout(request):
    order = Order.objects.all()
    return render(request, 'swirl/order_history.html',{'order':order})

def cart_detail(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = OrderItem.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
    else:
        items =[]
    return render(request, 'swirl/cart_detail.html',{'items':items})
