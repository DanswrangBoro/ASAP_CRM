# Generated by Django 5.0.2 on 2024-03-16 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0014_remove_chargeback_chargeback_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='card_number',
            field=models.IntegerField(default='1234567890123456', max_length=16),
        ),
    ]
