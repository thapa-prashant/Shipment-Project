from django.urls import path
from .views import *

app_name = "shipmentapp"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('send-notification/', SendNotificationView.as_view(), name="sendnotification"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('all-shipments/', AllShipmentsView.as_view(), name="allshipments"),
    path('request-shipment/', RequestShipmentView.as_view(), name="requestshipment"),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
]