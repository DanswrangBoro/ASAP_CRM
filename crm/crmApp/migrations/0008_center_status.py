# Generated by Django 5.0.2 on 2024-03-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0007_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=10),
        ),
    ]
