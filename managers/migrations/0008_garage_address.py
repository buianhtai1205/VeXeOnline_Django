# Generated by Django 4.1.3 on 2022-11-30 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0007_rename_desciption_garage_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='garage',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
    ]