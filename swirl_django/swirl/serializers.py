from rest_framework import serializers
from .models import Item, Order, OrderItem

class ItemSerializer(serializers.HyperlinkedModelSerializer):

   class Meta:
       model = Item
       fields=('id','title','description','ingredients', 'price','espresso','milk','shot','customize','img_url','preview_url',)

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.HyperlinkedRelatedField(
        view_name='item_detail',
        read_only=True
    )
    class Meta:
       model = OrderItem
       fields=('id','item','quantity','ordered',)

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # items = serializers.HyperlinkedRelatedField(
    #     view_name='item_detail',
    #     read_only=True
    # )
    class Meta:
       model = Order
       fields=('id','start_date','ordered_date','ordered',)