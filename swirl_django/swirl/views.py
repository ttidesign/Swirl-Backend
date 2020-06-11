from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Item, OrderItem, Order, Customer, ShippingAddress
from .serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, UserSerializer, CustomerSerializer
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json
import datetime
from .utils import cookieCart
# Create your views here.



# class CustomerList(generics.ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ItemList(generics.ListCreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

# class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

# class OrderItem(generics.ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

# class Order(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
        

def store(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        # items =[]
        # order = {'get_cart_total':0,'get_cart_items':0}
        # cartItems = order['get_cart_items']
        
    items = Item.objects.all()
    context={'items':items, 'cartItems':cartItems}
    return render(request, 'swirl/store.html',context)

def item_detail(request,pk):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    item = Item.objects.get(id=pk)
    context={'item':item,'cartItems':cartItems}
    return render(request, 'swirl/item_detail.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        # items =[]
        # order = {'get_cart_total':0,'get_cart_items':0}
    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'swirl/checkout.html',context)

def cart_detail(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,ordered=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'swirl/cart_detail.html',context)

# @csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action',action)
    print('productId',productId)
    customer = request.user.customer 
    # customer = data['user']['customer'] or data['user']['username']
    # print(data['user'])
    item = Item.objects.get(id=productId)
    # print(item)
    order, created = Order.objects.get_or_create(customer=customer,ordered=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,item=item)
    print(order)
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