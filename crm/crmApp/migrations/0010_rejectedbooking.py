# Generated by Django 5.0.2 on 2024-03-07 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0009_user_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='RejectedBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('reason', models.TextField()),
                ('rejection_date', models.DateField(auto_now_add=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crmApp.booking')),
            ],
        ),
    ]
