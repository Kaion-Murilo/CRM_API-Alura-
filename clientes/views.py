from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer
from rest_framework.authentication import TokenAuthentication
# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("Usuário:", request.user)
        print("Auth:", request.auth)

        return super().list(request, *args, **kwargs)