from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from clientes.views import ClientViewSet
from django.views.generic import TemplateView
router = routers.DefaultRouter()
router.register('clientes', ClientViewSet, basename='clientes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/', include(router.urls)),
]



