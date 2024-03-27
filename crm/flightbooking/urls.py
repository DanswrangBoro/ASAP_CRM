from django.urls import path
from . import views

app_name='flightbooking'

urlpatterns = [
    path("",views.flightbook,name="bookform"),
    path('flight.search/',views.flight_search_view,name="flight_search"),
    path('originsearch/', views.origin_search, name="origin_search"),
    path('destinationsearch/', views.destination_search, name='destination_search'),
    path('customCredentials/',views.customCredentials, name='customCredentials'),
    path('customCredentialsMulti/',views.customCredentialsMulti, name='customCredentialsMulti'),
    path('search.availability/',views.search_availability, name='search_available'),
    path('seatmap/',views.seatmapView,name='seatmap'),
    path('seatmapMulti/',views.seatmapViewMulti,name='seatmapmulti'),
    path('create_orders/',views.create_orders,name='create_order'),
    path('create_orders_multi/',views.create_orders_multi,name='create_order_multi'),
    path('order_complete/',views.thankyou_page,name='thankyou_page'),
    path('code-lookup/',views.airline_code_lookup,name = 'code_lookup'),
    path('seatmap.select/',views.seatMapTemplateView, name = "seatmap-select"),
    path('price.summary/',views.summary, name="summary"),
    path('price.summary_multi/',views.summary_multi, name="summary_multi"),
    path('searc_multi_city/', views.multiCitySearch, name="multiSearch"),
    path('multi_offer_price/',views.offers_search_multicity, name="multiOfferSearch"),
]