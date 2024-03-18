from django.test import TestCase
from django.utils import timezone
from .models import Booking, Chargeback

class BookingModelTestCase(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            booking_id='TEST123',
            confirmation_no='CONF123',
            passenger_name='John Doe',
            phone_number='1234567890',
            email='john@example.com',
            flight_details='Flight ABC123',
            trip_type='One-way',
            reference_id='REF123',
            departure='City A',
            departure_date=timezone.now(),
            arrival='City B',
            arrival_date=timezone.now(),
            num_passengers=1,
            price=100.00,
            status='pending',
            lead_agent=None,
            card_number=1234567890123456
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.passenger_name, 'John Doe')
        self.assertEqual(self.booking.price, 100.00)
        self.assertIsNone(self.booking.lead_agent)
        # Add more assertions for other fields as needed

class ChargebackModelTestCase(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            booking_id='TEST123',
            confirmation_no='CONF123',
            passenger_name='John Doe',
            phone_number='1234567890',
            email='john@example.com',
            flight_details='Flight ABC123',
            trip_type='One-way',
            reference_id='REF123',
            departure='City A',
            departure_date=timezone.now(),
            arrival='City B',
            arrival_date=timezone.now(),
            num_passengers=1,
            price=100.00,
            status='pending',
            lead_agent=None,
            card_number=1234567890123456
        )
        self.chargeback = Chargeback.objects.create(
            Booking=self.booking,
            credit_card_no='1234-5678-9012-3456',
            confirmation_mail_status='sent',
            reason='Fraudulent transaction',
            chargeback_received_date=timezone.now(),
            chargeback_status='pending',
            chargeback_lead_status='pending'
        )

    def test_chargeback_creation(self):
        self.assertEqual(self.chargeback.reason, 'Fraudulent transaction')
        self.assertEqual(self.chargeback.chargeback_status, 'pending')
        # Add more assertions for other fields as needed
