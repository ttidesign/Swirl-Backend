# Generated by Django 3.0.7 on 2020-06-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swirl', '0004_auto_20200610_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
