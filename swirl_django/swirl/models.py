from django.db import models

# Create your models here.
Espresso = (
    ('signature','Espresso Signature Blend'),
    ('blonde','Espresso blonde'),
    ('darkroasted','Darkroasted bean'),
    ('none','None'),
)
Milk = (
    ('2% Milk','2%'),
    ('non-fat','Non-fat'),
    ('soy','Soy')
    )
Shot = (
    ('double','Double'),
    ('triple','Triple'),
    ('quadruple','Quadruple'),
    ('none','None')
)
class Drink(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
