from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Client, Note
from .serializers import ClientSerializer, NoteSerializer,UserSerializer
from .permissions import IsAdminOrOwner
from rest_framework import filters
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
class UserCreateView(generics.CreateAPIView):
    """
    POST /api/register/ → cria um novo vendedor
    Qualquer um pode se registrar; será adicionado ao grupo Vendedor automaticamente.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # AllowAny → qualquer pessoa (logada ou não) pode se registrar.


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    # ↑ exige autenticação E (admin OU proprietário)
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name', 'email', 'phone', 'status']
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(responsavel=self.request.user)
    
    def perform_create(self, serializer):
        # ← ADICIONE ESTA FUNÇÃO
        serializer.save(responsavel=self.request.user)
    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            serializer.validated_data['responsavel'] = self.get_object().responsavel
        serializer.save()
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    # ↑ mesma permissão
    
    def get_queryset(self):
        client_id = self.kwargs['client_id']
        client = Client.objects.get(id=client_id)
        
        # Valida se o usuário tem acesso ao cliente
        if self.request.user.is_superuser or client.responsavel == self.request.user:
            return Note.objects.filter(client_id=client_id)
        
        # Se não é admin e não é o responsável, retorna vazio
        return Note.objects.none()
    
    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        client = Client.objects.get(id=client_id)
        serializer.save(responsavel=self.request.user)