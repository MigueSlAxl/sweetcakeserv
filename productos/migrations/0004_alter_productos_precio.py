# Generated by Django 3.2.18 on 2023-04-28 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_productos_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='precio',
            field=models.CharField(max_length=20),
        ),
    ]
