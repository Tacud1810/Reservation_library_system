# Generated by Django 4.2.3 on 2023-07-10 13:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("viewer", "0006_cart_complete_alter_cartitem_cart"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Cart",
            new_name="Order",
        ),
        migrations.RenameModel(
            old_name="CartItem",
            new_name="OrderItem",
        ),
    ]