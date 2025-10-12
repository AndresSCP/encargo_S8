# SEMANA8/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluye las rutas de tu app (páginas y API v1/)
    # IMPORTANTE: solo una vez; NO repetir con 'api/' también.
    path('', include('ImpoVinos.urls')),

    # Endpoints JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
