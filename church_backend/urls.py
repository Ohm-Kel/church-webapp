"""
URL configuration for church_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views 
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from core.views import RegisterView, UserProfileView


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token endpoints
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me/', UserProfileView.as_view(), name='user-profile'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair_alias'),

    path('api/', include('core.urls')),
    path('', views.home, name='home'),
    
    
]

schema_view = get_schema_view(
    openapi.Info(
        title="Church WebApp API",
        default_version='v1',
        description="REST API for Executive Members, Events, Personalities, Sermons, and Members",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    # Raw JSON schema
    path('swagger.json',
         schema_view.without_ui(cache_timeout=0),
         name='schema-json'),

    # Swagger UI
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    # ReDoc UI
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]



