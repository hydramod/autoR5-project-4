# Generated by Django 4.2.5 on 2023-10-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoR5', '0008_alter_car_car_type_alter_car_fuel_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='features',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
