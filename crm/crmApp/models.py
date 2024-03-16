from django.db import models
from asyncio.windows_events import NULL
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class PNR_TABLE(models.Model):
    email = models.TextField(max_length=200)
    phone = models.TextField(max_length=10)
    ref_id = models.TextField(max_length=200)
    address = models.TextField(max_length = 255,default="")
    zip = models.TextField(max_length = 200)
    city = models.TextField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
    
    

class Price_manipulation_percentage(models.Model):
    price = models.IntegerField(max_length=100)


class Price_manipulation_amount(models.Model):
    price = models.IntegerField(max_length=1000)

class MarkupControl(models.Model):
    TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='percentage')
    activation = models.BooleanField(default=False)

    def __str__(self):
        return f"Type: {self.type}, Activation: {self.activation}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists for each type
        existing_instances = MarkupControl.objects.filter(type=self.type)
        if self.activation is False:
            # If activation is set to False, set activation of the other type to True
            other_type = 'percentage' if self.type == 'amount' else 'amount'
            other_instance = existing_instances.exclude(pk=self.pk).first()
            if other_instance:
                other_instance.activation = True
                other_instance.save()

        super().save(*args, **kwargs)

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phoneNumber = models.CharField(max_length=15)
    role = models.CharField(max_length=20)
    team = models.CharField(max_length=100)
    blocked = models.BooleanField(default=False)

    # Add related_name to avoid clash with default User model
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True, verbose_name='user permissions')

    def __str__(self):
        return self.username

class Booking(models.Model):
    booking_id = models.CharField(max_length=100)
    confirmation_no = models.CharField(max_length=255,null=True,blank=True)
    passenger_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    flight_details = models.CharField(max_length=255)
    trip_type = models.CharField(max_length=50)
    reference_id = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    departure_date = models.DateField()
    arrival = models.CharField(max_length=100)
    arrival_date = models.DateField()
    num_passengers = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    change_date = models.DateTimeField(blank=True, null=True)
    mco = models.CharField(max_length=100, blank=True, null=True)
    lead_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='lead_bookings')
    card_number = models.IntegerField(max_length=16,default="1234567890123456")

    def __str__(self):
        return self.booking_id



class Refund(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_reason = models.TextField()
    status = models.CharField(max_length=20,default="Pending")

    def __str__(self):
        return f"Refund for Booking ID: {self.booking.booking_id}"


# ==================================================================user model=====================
    
# class Person(models.Model):
#     user_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=15)
#     role = models.CharField(max_length=10, choices=[('manager', 'Manager'), ('agent', 'Agent')])
#     team = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     blocked = models.BooleanField(default=False)  # New field for storing block status
#     last_login = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return self.user_name




# ===============================================================reject model================================
    
class RejectedBooking(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()
    rejection_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Rejected Booking: {self.customer_name}"

#================================================================end reject model=============================

# ===============================================================slaes model==================================
class Sale(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sale_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

    def __str__(self):
        return f"Sale by {self.agent.username} on {self.sale_date}"

# ===============================================================sales model==================================


# ==============================================================================( Chargeback Model)=============================

class Chargeback(models.Model):
    Booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, related_name='lead_bookings')
    credit_card_no = models.CharField(max_length=20)
    confirmation_mail_status = models.CharField(max_length=50)
    reason = models.CharField(max_length=100)
    chargeback_received_date = models.DateField()
    chargeback_status = models.CharField(max_length=50, default="pending")
    chargeback_lead_status = models.CharField(max_length=50, default="pending")
    def __str__(self):
        return f"Chargeback for {self.Booking.booking_id}"
# ==============================================================================( End Chargeback Model)=============================