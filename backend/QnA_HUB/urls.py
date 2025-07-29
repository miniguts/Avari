from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('askly.urls')),
    path('api/schema/', SpectacularAPIView.as_view(),
         name='schema'),
    path('api/schema/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
