from django.urls import path
from . import views
from .views import update_booking_status
from .views import fetch_passenger_name

app_name = 'crmApp'

urlpatterns = [
    path('base/', views.flight_book, name='base'),
    path('total_booking/', views.total_booking, name='total_booking'),
    path('total_user/', views.total_user, name='total_user'),
    path('booking/', views.booking, name='booking'),
    path('refund/', views.refund, name='refund'),
    path('chargeback/', views.chargeback, name='chargeback'),
    path('rejected/', views.rejected, name='rejected'),
    path('mco/', views.mco, name='mco'),
    path('cancellation/', views.cancellation, name='cancellation'),
    path('ecredit/', views.ecredit, name='ecredit'),
    path('update_booking_status/', update_booking_status, name='update_booking_status'),
    path('fetch_passenger_name/', fetch_passenger_name, name='fetch_passenger_name'),
]



