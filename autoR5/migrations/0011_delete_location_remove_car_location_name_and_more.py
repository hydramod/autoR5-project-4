# Generated by Django 4.2.5 on 2023-10-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoR5', '0010_booking_status_alter_car_features_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.RemoveField(
            model_name='car',
            name='location_name',
        ),
        migrations.AddField(
            model_name='cancellationrequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='car',
            name='location_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='location_city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_intent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed'), ('Refunded', 'Refunded')], default='Pending', max_length=20),
        ),
    ]
