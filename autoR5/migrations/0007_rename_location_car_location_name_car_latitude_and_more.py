# Generated by Django 4.2.5 on 2023-10-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoR5', '0006_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='location_name',
            new_name='location_name',
        ),
        migrations.AlterField(
            model_name='car',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=53.349805, max_digits=9),
        ),
        migrations.AlterField(
            model_name='car',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=-6.26031, max_digits=9),
        ),
    ]
