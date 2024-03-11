from django.urls import path
from . import views
from .views import update_booking_status
from .views import fetch_passenger_data,submit_refund_form,update_refund_status
from django.contrib.auth.views import LoginView

app_name = 'crmApp'

urlpatterns = [
    path('', views.login_view, name='login'),  # Assign 'login' as the name for the login view
    path('base/', views.flight_book, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
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
    path('fetch_passenger_data/', fetch_passenger_data, name='fetch_passenger_data'),
    path('submit_refund_form/', submit_refund_form, name='submit_refund_form'),
    path('get_location_suggestions/', views.get_location_suggestions, name='get_location_suggestions'),
    path('flight_results/', views.flight_results, name='flight_results'),
    path('update_refund_status/', update_refund_status, name='update_refund_status'),
    path('create_user/', views.create_user, name='create_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('logout/', views.logout_view, name='logout'),
    # path('update_booking_statusT/', views.update_booking_statusT, name='update_booking_statusT'),
    path('delete_booking/', views.delete_booking, name='delete_booking'),
    path('grant_permissions/', views.grant_permissions, name='grant_permissions'),



]



