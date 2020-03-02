from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf import settings
from django.contrib import admin
from shipmentapp.views import Demoview
urlpatterns = [
    re_path('^.*',Demoview.as_view(),name="demo"),
    path('django-admin/', admin.site.urls),
    path('home/', include('shipmentapp.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)