# Generated by Django 4.2.5 on 2023-10-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoR5', '0017_alter_car_car_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_type',
            field=models.CharField(blank=True, choices=[('Hatchback', 'Hatchback'), ('Saloon', 'Saloon'), ('Estate', 'Estate'), ('MPV', 'MPV'), ('SUV', 'SUV'), ('Sports_Car', 'Sports_Car')], max_length=20, null=True),
        ),
    ]
