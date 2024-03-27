from django.urls import URLPattern, path
from . import views

app_name='countries'

urlpatterns = [
    path("<str:country_name>/", views.countries, name ="country"),
    # path("login/", views.user_login, name ="login"),
]