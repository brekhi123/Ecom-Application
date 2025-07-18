from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', include('customadmin.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path ('dj-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
