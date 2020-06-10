from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
Espresso_Choices = (
    ('signature','Espresso Signature Blend'),
    ('blonde','Espresso Blonde'),
    ('darkroasted','Espresso Darkroasted'),
    ('none','None'),
)
Milk_Choices = (
    ('2% Milk','2%'),
    ('non-fat','Non-fat'),
    ('soy','Soy')
    )
Shot_Choices = (
    ('double','Double'),
    ('triple','Triple'),
    ('quadruple','Quadruple'),
    ('none','None')
)
#Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

#drink/product model
class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.CharField(max_length=300)
    price = models.FloatField(default=5)
    espresso = models.CharField(choices=Espresso_Choices, default='Espresso Signature Blend', max_length=20)
    milk = models.CharField(choices=Milk_Choices,default='2%', max_length=20)
    shot = models.CharField(choices=Shot_Choices, default='double', max_length=20)
    customize = models.CharField(max_length=100,default='none')
    img_url = models.TextField()
    preview_url = models.TextField()

    def __str__(self):
        return self.title
    

#order model
class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)

    # @property

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#list of drinks add to order become list of order item
class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return self.item.title
    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address