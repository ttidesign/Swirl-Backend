# Generated by Django 3.0.7 on 2020-06-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swirl', '0005_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
        ),
    ]
