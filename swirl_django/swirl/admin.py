from django.contrib import admin

# Register your models here.
from .models import Item, OrderItem, Order, Customer, ShippingAddress

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(ShippingAddress)