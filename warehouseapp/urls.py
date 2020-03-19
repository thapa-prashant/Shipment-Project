from django.urls import path
from .views import *

app_name = "warehouseapp"

urlpatterns = [
    path("warehouse/logistic-admin/home/", WareHouseHomeView.as_view(), 
        name = "warehousehome"),

    path("warehouse/logistic-admin/login/", WareHouseAdminLoginView.as_view(), 
        name = "warehouseadminlogin"),
    path('warehouse/logistic-admin/logout/', WareHouseAdminLogoutView.as_view(), 
        name = "warehouseadminlogout"),

    path('warehouse/logistic-admin/profile-info/', WareHouseAdminProfileView.as_view(), 
        name = "warehouseadminprofile"),

    path('warehouse/logistic-admin/all-staffs/list/', WareHouseAdminStaffListView.as_view(), 
        name = "warehouseadminstafflist"),
    
    path('warehouse/logistic-admin/all-shipments/list/', WareHouseAdminShipmentListView.as_view(), 
        name = "warehouseadminshipmentlist"),

    path('warehouse/logistic-admin/shipment-location/list/', WareHouseAdminShipmentLocationListView.as_view(), 
        name = "warehouseadminshipmentlocationlist"),

    # path('warehouse/logistic-admin/new-shipment-location/list/', WareHouseAdminNewShipmentLocationListView.as_view(), 
    #     name = "warehouseadminnewshipmentlocationlist"),

    
    
]