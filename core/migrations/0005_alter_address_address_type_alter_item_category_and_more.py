# Generated by Django 5.0.6 on 2024-06-11 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_address_address_type_alter_item_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('S', 'Shipping'), ('B', 'Billing')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('SW', 'Sport wear'), ('S', 'Shirt'), ('OW', 'Outwear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('S', 'secondary'), ('D', 'danger'), ('P', 'primary')], max_length=1),
        ),
    ]
