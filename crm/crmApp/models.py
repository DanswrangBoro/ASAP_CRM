from django.db import models
from asyncio.windows_events import NULL
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


# ==========================================================================( €Centers Start)=======================================

class Center(models.Model):
    # Other fields...
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=100)
    document = models.FileField(upload_to='center_documents/', null=True, blank=True)
    
    # New field for status
    ACTIVE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=ACTIVE_STATUS_CHOICES, default='inactive')

    def __str__(self):
        return self.name


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
    ROLE_CHOICES = [
        ('manager', 'manager'),
        ('agent', 'agent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    blocked = models.BooleanField(default=False)

    # Foreign key to Center
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

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
    lead_agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_bookings')
    card_number = models.IntegerField(max_length=16,default="1234567890123456")
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.booking_id
    def natural_key(self):
            return (
                self.booking_id, self.confirmation_no, self.passenger_name,
                self.phone_number, self.email, self.flight_details,
                self.trip_type, self.reference_id, self.departure,
                self.departure_date.isoformat(), self.arrival,
                self.arrival_date.isoformat(), self.num_passengers,
                str(self.price), self.status, 
                self.change_date.isoformat() if self.change_date else None,
                self.mco, self.lead_agent.natural_key() if self.lead_agent else None,
                self.card_number
            )



class Refund(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_reason = models.TextField()
    refund_type =  models.CharField(max_length=20,null = True, blank= True)
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
    

# =================================================================================(submit invoice)==========================



class Invoice(models.Model):
    invoice_id = models.CharField(max_length=255, default="", null= True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, default="")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    markup_price = models.DecimalField(max_digits=10, decimal_places=2)
    description1 = models.CharField(max_length=100)
    total1 = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    description2 = models.CharField(max_length=100)
    total2 = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")
    def __str__(self):
        return self.invoice_id
    def natural_key(self):
        return (
            self.invoice_id, self.booking.natural_key(), str(self.base_price),
            str(self.markup_price), self.description1, str(self.total1),
            str(self.tax), self.description2, str(self.total2),
            str(self.discount), str(self.total_discount), str(self.grand_total)
        )
    def addition_charges(self):
        return self.additioncharge_set.all()


class AdditionCharge(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, default="")
    price = models.FloatField()
    description = models.CharField(max_length=255)
    def natural_key(self):
        return (self.invoice.natural_key(), str(self.price), self.description)


# ====================================================================( dropbox sign ) ========================
    
class Payment(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    transaction_status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    cardholder_name = models.CharField(max_length=100)
    card_number = models.IntegerField(max_length=16, validators=[MaxValueValidator(9999999999999999), MinValueValidator(1000000000000000)])
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment for Booking ID: {self.booking}"
    
class MCO(models.Model):
    booking = models.ForeignKey('Booking', on_delete= models.CASCADE)
    price = models.FloatField(null=True, blank = True)




    # New field for acknowledgment status
    ACKNOWLEDGEMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
    ]
    acknowledgment_status = models.CharField(max_length=20, choices=ACKNOWLEDGEMENT_STATUS_CHOICES, default='pending')
    signed_at = models.CharField(max_length=20,default='Not signed yet', blank=True, null=True)
    def __str__(self):
        return self.name

