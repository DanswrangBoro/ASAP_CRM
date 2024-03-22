from django.urls import path
from . import views
from .views import centersList, pending_invoices, relatedBooking, send_signature_request, update_booking_status
from .views import fetch_passenger_data,submit_refund_form,update_refund_status
from django.contrib.auth.views import LoginView
from .views import reassign_lead_agent


app_name = 'crmApp'

urlpatterns = [
    path('', views.login_view, name='login'),  # Assign 'login' as the name for the login view
    # path('base/', views.flight_book, name='base'),
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
    path('book_view/', views.book_view, name='book_view'),
    path('generate-invoice/', views.generate_invoice, name='generate_invoice'),
    path('send-email/', views.send_email, name='send_email'),
    # path('invoice-success/', invoice_success, name='invoice_success'),
    path('sales/', views.sales_view, name='sales'),
    path('reassign/', reassign_lead_agent, name='reassign_lead_agent'),
    path('get_agent_data/', views.get_agent_data, name='get_agent_data'),
    path('check-availability/', views.check_flight, name='check-flight'),    path('submit_chargeback/', views.submit_chargeback, name='submit_chargeback'),
    path('update_chargeback_lead_status/', views.update_chargeback_lead_status, name='update_chargeback_lead_status'),
    path('update_chargeback_status/', views.update_chargeback_status, name='update_chargeback_status'),
    # path('chargeback-details/<int:chargeback_id>/', views.chargeback_details, name='chargeback_details'),
    path('invoice/', views.invoiceCreate, name='invoice'),
    path('submit-invoice/', views.submit_invoice, name='submit_invoice'),
    path('fetch-invoice/', views.invoice_details_fetch, name="invoice-details-fetch"),
    path('submit_form_customer/', views.submit_cutomer, name = 'submit_customer'),
    path('send-signature-request/', send_signature_request, name='send_signature_request'),
    path('pending_invoices/', pending_invoices, name='pending_invoices'),
    path('flight-search-multi/', views.flight_search_multi, name='multi_search'),
    path('payment/', views.payment, name='payment'), 
    path('related-booking/', relatedBooking, name='related_booking'),
    path('initiate-payment/', views.initiatePayment, name='initiatePayment'),
    path('invoice-form/', views.invoice_form, name="invocie_form"),
    path('gateway/', views.gateway, name='gateway'),
    path('centers/', centersList, name='centers_list'),
    path('add-center/', views.add_center, name='add_center'),
    path('centers/<int:id>/pdf/', views.view_pdf, name='view_pdf'),
]



