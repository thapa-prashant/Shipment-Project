from django.urls import path
from .views import *

app_name = "shipmentapp"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('all-shipments/', AllShipmentsView.as_view(), name="allshipments"),
]