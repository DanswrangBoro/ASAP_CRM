# Generated by Django 5.0.2 on 2024-03-12 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0002_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='lead_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]