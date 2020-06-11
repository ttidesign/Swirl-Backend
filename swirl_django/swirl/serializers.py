from rest_framework import serializers
from .models import Item, Order, OrderItem, Customer
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ('id','username','email','first_name','customer',)

class CustomerSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = Customer
        fields = ('id','user','name','email',)

class ItemSerializer(serializers.ModelSerializer):
    espresso = serializers.SerializerMethodField()
    milk = serializers.SerializerMethodField() 
    shot = serializers.SerializerMethodField()  
    class Meta:
       model = Item
       fields=('id','title','description','ingredients', 'price','espresso','milk','shot','customize','img_url','preview_url',)
    def get_espresso(self,obj):
        return obj.get_espresso_display()
    def get_milk(self,obj):
        return obj.get_milk_display()
    def get_shot(self,obj):
        return obj.get_shot_display()    

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
       model = OrderItem
       fields=('id','item','quantity',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
       model = Order
       fields=('id','customer','start_date','ordered_date','ordered','transaction_id',)
