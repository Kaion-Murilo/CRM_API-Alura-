from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from clientes.views import ClientViewSet,NoteViewSet,UserCreateView
from django.views.generic import TemplateView
router = routers.DefaultRouter()
router.register('clientes', ClientViewSet, basename='clientes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/', include(router.urls)),
       # Rotas de Notas
    path('api/clientes/<uuid:client_id>/notas/', NoteViewSet.as_view({'get': 'list', 'post': 'create'}), name='note-list'),
    # GET  /api/clientes/6dde0e47.../notas/      → lista
    # POST /api/clientes/6dde0e47.../notas/      → cria
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    # POST /api/register/ → cria novo vendedor
    path('api/clientes/<uuid:client_id>/notas/<uuid:pk>/', NoteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='note-detail'),
    # GET    /api/clientes/6dde0e47.../notas/5.../  → detalha
    # PUT    /api/clientes/6dde0e47.../notas/5.../  → atualiza
    # DELETE /api/clientes/6dde0e47.../notas/5.../  → deleta
    
    path('', TemplateView.as_view(template_name='index.html')),
]



