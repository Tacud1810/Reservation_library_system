# Generated by Django 4.2.3 on 2023-07-05 05:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("viewer", "0002_alter_author_birth_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="added",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
