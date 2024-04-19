from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from links.routers import user_link_router, user_link_collection_router
from users.routers import custom_user_router
from users.JWT_views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView, DecoratedTokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="Links storage (X_One test task)",
        default_version='v1',
        description="API for storing and distributing to collections of custom links. When adding a link to the system,"
                    " the system generates a title, description, link type and so on for user convenience.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('api/auth/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Авторизация JWT
    path('api/auth/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(custom_user_router.urls)),
    path('api/', include(user_link_router.urls)),
    path('api/', include(user_link_collection_router.urls)),

    path('api/documentation/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/documentation/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
