from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.utils import timezone
from rest_framework import generics
from .serializers import ItemSerializer, OrderItemSerializer 
# Create your views here.
# def item_list(request):
#     items = Item.objects.all()
#     return render(request, 'swirl/item_list.html',{'items':items})

# def item_list(request):
#     items = Item.objects.all().values('title', 'description', 'img_url')
#     items_list = list(items)
#     return JsonResponse(items_list, safe=False)
class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderItem(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# class Order(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

def item_detail(request,pk):
    item = Item.objects.get(id=pk)
    return render(request, 'swirl/item_detail.html',{'item':item})

def order_detail(request):
    order = Order.objects.all()
    return render(request, 'swirl/order_history.html',{'order':order})

def add_to_cart(request,pk):
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
        else: 
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)