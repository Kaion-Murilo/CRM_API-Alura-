from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, Note
from .serializers import ClientSerializer, NoteSerializer
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name', 'email', 'phone', 'status']
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes → exige autenticação para todas as operações.
    
    def get_queryset(self):
        # Retorna apenas as notas do cliente especificado na URL.
        client_id = self.kwargs['client_id']
        return Note.objects.filter(client_id=client_id)
    
    def perform_create(self, serializer):
        # Ao criar uma nota, preenchê automaticamente o usuário logado.
        client_id = self.kwargs['client_id']
        client = Client.objects.get(id=client_id)
        serializer.save(user=self.request.user, client=client)
        # user=self.request.user → quem está logado criou a nota.