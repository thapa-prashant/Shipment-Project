from django.urls import path
from .views import *

app_name = "shipmentapp"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('send-notification/', SendNotificationView.as_view(), name="sendnotification"),
    path('login/', LoginView.as_view(), name="login"),
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('update/', UserUpdateView.as_view(), name="userupdate"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('all-shipments/', AllShipmentsView.as_view(), name="allshipments"),
    path('request-shipment/', RequestShipmentView.as_view(), name="requestshipment"),
    path('password-change/',PasswordChangeView.as_view(),name="changepassword"),
]