# Generated by Django 4.1.3 on 2022-11-28 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0005_alter_trip_departure_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='garage_id',
            new_name='garage',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='garage_id',
            new_name='garage',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='trip_id',
            new_name='trip',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='schedule_id',
            new_name='schedule',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='seat_id',
            new_name='seat',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='trip_id',
            new_name='trip',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='garage_id',
            new_name='garage',
        ),
    ]
