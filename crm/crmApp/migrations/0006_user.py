# Generated by Django 5.0.2 on 2024-03-06 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmApp', '0005_rename_booking_refund_booking_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('role', models.CharField(choices=[('superadmin', 'Super Admin'), ('user', 'User')], max_length=10)),
                ('team', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]