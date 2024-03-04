from django.db import models

from django.db import models

class Booking(models.Model):
    booking_id = models.CharField(max_length=100)
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

    def __str__(self):
        return self.booking_id


class Refund(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_reason = models.TextField()

    def __str__(self):
        return f"Refund for Booking ID: {self.booking.booking_id}"
