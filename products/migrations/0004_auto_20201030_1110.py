# Generated by Django 3.1.2 on 2020-10-30 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
