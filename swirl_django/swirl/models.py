from django.db import models
from django.conf import settings

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


#drink model
class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.CharField(max_length=300)
    price = models.FloatField()
    espresso = models.CharField(choices=Espresso_Choices, default='Espresso Signature Blend', max_length=20)
    milk = models.CharField(choices=Milk_Choices,default='2%', max_length=20)
    shot = models.CharField(choices=Shot_Choices, default='double', max_length=20)
    customize = models.CharField(max_length=100,default='none')
    img_url = models.TextField()
    preview_url = models.TextField()

    def __str__(self):
        return self.title


#list of drinks add to order become list of order item
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


#order model associate with users
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
