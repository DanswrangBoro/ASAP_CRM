# Generated by Django 5.0.2 on 2024-03-16 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0012_booking_confirmation_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chargeback',
            name='booking_confirmation_no',
        ),
    ]
