from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = "Nepal Tourism E-Governance Portal"
admin.site.site_title = "Nepal Tourism Admin"
admin.site.index_title = "Department of Tourism — Administration Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('accounts/', include('accounts.web_urls')),
    path('destinations/', include('destinations.urls')),
    path('bookings/', include('bookings.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)