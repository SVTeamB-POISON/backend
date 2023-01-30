from django.contrib import admin
from django.urls import path, include ,re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="poison",
        default_version='1.0',
        description="api 세팅",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'api/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'api/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'api/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('api/admin/', admin.site.urls),
    path('api/flowers/', include('flower.urls')),
    path("api/",include("django_prometheus.urls"))

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

