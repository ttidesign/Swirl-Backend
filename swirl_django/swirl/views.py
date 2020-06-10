from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Item, OrderItem, Order, Customer, ShippingAddress
from django.http import JsonResponse
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST 
from .serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, UserSerializer, CustomerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# class OrderItem(generics.ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

# class Order(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# @permission_classes((permissions.AllowAny,))
# class AddToCartView(APIView):
#     def post(self,request):
#         pk = request.data.get('id',None)
#         if pk is None:
#             return Response({'message':'Invalid request'}, status=HTTP_400_BAD_REQUEST)
#         item = get_object_or_404(Item, pk=item.pk)
#         order_item, created = OrderItem.objects.get_or_create(item=item,
#         user=request.user,
#             ordered=False)
#         order_qs = Order.objects.filter(user=request.user, ordered=False)
#         if order_qs.exists():
#             order = order_qs[0]
#             #check if there is any item in order
#             if order.items.filter(item__pk=item.pk).exists():
#                 order_item.quantity +=1
#                 order_item.save()
#                 return Response(status=HTTP_200_OK)
#             else: 
#                 order.item.add(order_item)
#                 return Response(status=HTTP_200_OK)
#         else:
#             ordered_date = timezone.now()
#             order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#             order.items.add(order_item)
#             return Response(status=HTTP_200_OK)
        
# def add_to_cart(request,pk):
#     item = get_object_or_404(Item, pk=pk)
#     order_item, created = OrderItem.objects.get_or_create(item=item,
#     user=request.user,
#         ordered=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         #check if there is any item in order
#         if order.items.filter(item__pk=item.pk).exists():
#             order_item.quantity +=1
#             order_item.save()
#         else: 
#             order.item.add(order_item)
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         return redirect('item_detail',pk=item.pk)

def store(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']
    items = Item.objects.all()
    context={'items':items, 'cartItems':cartItems}
    return render(request, 'swirl/store.html',context)

def item_detail(request,pk):
    item = Item.objects.get(id=pk)
    return render(request, 'swirl/item_detail.html',{'item':item})

def checkout(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0}
    context={'items':items, 'order':order}
    return render(request, 'swirl/checkout.html',context)

def cart_detail(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0}
    context={'items':items, 'order':order}
    return render(request, 'swirl/cart_detail.html',context)

# @csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action',action)
    print('productId',productId)
    print(data)
    customer = request.user.customer or request.user.id
    item = Item.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,ordered=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,item=item)
    if action =='add':
        orderItem.quantity= (orderItem.quantity +1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('item was add',safe=False)

def processOrdder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            print(total)
            order.ordered = True
            order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        print('User is not logged in')
    return JsonResponse('Payment complete!', safe=False)

# @permission_classes((permissions.AllowAny,))
# class AddToCartView(APIView):
#     def updateItem(request):
#         data = json.loads(request.body)
#         productId = data['productId']
#         action = data['action']
#         print('Action',action)
#         print('productId',productId)
#         customer = request.user.customer
#         item = Item.objects.get(id=productId)
#         order, created = Order.objects.get_or_create(customer=customer,ordered=False)
#         orderItem,created = OrderItem.objects.get_or_create(order=order,item=item)
#         if action =='add':
#             orderItem.quantity= (orderItem.quantity +1)
#         elif action =='remove':
#             orderItem.quantity = (orderItem.quantity -1)
#         orderItem.save()
#         if orderItem.quantity <=0:
#             orderItem.delete()
#         return JsonResponse('item was add',safe=False)